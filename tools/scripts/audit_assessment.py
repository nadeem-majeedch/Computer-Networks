#!/usr/bin/env python3
"""Assessment-package audit for the Computer Networks course repository.

Run from the repository root:  python tools/scripts/audit_assessment.py
Validates assessments/: file inventory, quiz/review/bank completeness, difficulty
and CLO tag validity, cross-instrument duplicate stems, exam mark-total
consistency, weighting caveat presence, key-fence separation, and relative-link
resolution. Also runs verify_assessment_numbers.py as the numeric gate.
Exit 0 = clean (warnings allowed); 1 = at least one FAIL. Stdlib only.
"""

import os
import re
import subprocess
import sys

ROOT = '.'
A = os.path.join(ROOT, 'assessments')

results = []


def add(name, status, detail):
    results.append((name, status, detail))


def rd(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def norm(s):
    return re.sub(r'\s+', ' ', s).strip().lower()


# ---------------------------------------------------------------- 1. inventory
EXPECTED = (
    [f'quizzes/quiz-w{i:02d}.md' for i in range(1, 17)] +
    [f'review/review-m{i}.md' for i in range(1, 9)] +
    ['banks/conceptual.md', 'banks/numerical-subnetting.md',
     'banks/packet-analysis.md', 'banks/routing-troubleshooting.md',
     'banks/short-answer.md', 'banks/long-answer.md', 'banks/practical.md'] +
    ['assignments/subnetting-problem-set-student.md',
     'assignments/subnetting-problem-set-instructor.md',
     'assignments/reliable-transport-project-student.md',
     'assignments/reliable-transport-project-instructor.md'] +
    ['exams/midterm-student.md', 'exams/midterm-instructor.md',
     'exams/final-student.md', 'exams/final-instructor.md'] +
    ['rubrics/practical-work-rubric.md', 'rubrics/capstone-rubric.md'] +
    ['README.md', 'clo-assessment-mapping.md', 'academic-integrity.md',
     'marking-guide.md'])
missing = [f for f in EXPECTED if not os.path.isfile(os.path.join(A, f))]
add('inventory', 'PASS' if not missing else 'FAIL',
    f'{len(EXPECTED)} expected files' if not missing else f'missing: {missing}')
inv_fail = 1 if missing else 0

# ------------------------------------------------------- 2. quizzes complete
q_missing, q_nofence = [], []
for i in range(1, 17):
    rel = f'quizzes/quiz-w{i:02d}.md'
    if not os.path.isfile(os.path.join(A, rel)):
        continue
    t = rd(os.path.join(A, rel))
    if '**Q1' not in t or '## Student questions' not in t:
        q_missing.append(rel)
    if 'INSTRUCTOR KEY' not in t:
        q_nofence.append(rel)
add('quiz-completeness', 'PASS' if not (q_missing or q_nofence) else 'FAIL',
    '16 quizzes, student+key each' if not (q_missing or q_nofence)
    else f'no-questions: {q_missing} no-key: {q_nofence}')
q_fail = 1 if (q_missing or q_nofence) else 0

# -------------------------------------------------------- 3. reviews complete
r_missing, r_nofence = [], []
for i in range(1, 9):
    rel = f'review/review-m{i}.md'
    if not os.path.isfile(os.path.join(A, rel)):
        continue
    t = rd(os.path.join(A, rel))
    if '## Questions' not in t or 'SELF-CHECK KEY' not in t:
        r_missing.append(rel)
add('review-completeness', 'PASS' if not r_missing else 'FAIL',
    '8 module sets with keys' if not r_missing else f'problems: {r_missing}')
r_fail = 1 if r_missing else 0

# --------------------------------------------- 4. banks: keys + tier coverage
banks = ['conceptual', 'numerical-subnetting', 'packet-analysis',
         'routing-troubleshooting', 'short-answer', 'long-answer', 'practical']
b_nofence, b_tiers = [], []
for b in banks:
    t = rd(os.path.join(A, 'banks', f'{b}.md'))
    if 'INSTRUCTOR KEY' not in t:
        b_nofence.append(b)
    tiers = set(re.findall(r'\[(B|I|A|E)\|', t))
    if len(tiers) < 4:
        b_tiers.append((b, sorted(tiers)))
add('bank-keys-tiers', 'PASS' if not (b_nofence or b_tiers) else 'FAIL',
    '7 banks keyed, all four difficulty tiers each'
    if not (b_nofence or b_tiers) else f'no-key: {b_nofence} thin-tiers: {b_tiers}')
b_fail = 1 if (b_nofence or b_tiers) else 0

# --------------------------------------------------- 5. tag validity (CLOs)
CLO_OK = {f'CLO{i}' for i in range(1, 9)}
bad_tags = []
for dirpath, _, files in os.walk(A):
    for fn in files:
        if not fn.endswith('.md'):
            continue
        p = os.path.join(dirpath, fn)
        for m in re.finditer(r'\[(?:B|I|A|E)\|(CLO[\d, ]*)\|', rd(p)):
            for clo in re.findall(r'CLO\d+', m.group(1)):
                if clo not in CLO_OK:
                    bad_tags.append((fn, clo))
add('tag-validity', 'PASS' if not bad_tags else 'FAIL',
    'CLO1-8 and B/I/A/E tags only' if not bad_tags else f'bad: {bad_tags[:8]}')
t_fail = 1 if bad_tags else 0

# ------------------------------------------- 6. duplicate stems across package
stems = {}
dups = []
for dirpath, _, files in os.walk(A):
    for fn in files:
        if not fn.endswith('.md'):
            continue
        rel = os.path.relpath(os.path.join(dirpath, fn), A).replace('\\', '/')
        if fn.endswith('-instructor.md'):
            continue  # keys repeat stems by design
        t = rd(os.path.join(dirpath, fn))
        for m in re.finditer(r'(?:\*\*(?:Q\d+|C-\d+|N-\d+|PA-\d+|RT-\d+|SA-\d+|'
                             r'LA-\d+|PR-\d+|[A-Z]\d+)\*\*|\d+\.\s\[)[^\n]{10,}',
                             t):
            stem = norm(m.group(0))[:60]
            if stem in stems and stems[stem] != rel:
                dups.append((stem, stems[stem], rel))
            stems.setdefault(stem, rel)
add('duplicate-stems', 'PASS' if not dups else 'FAIL',
    f'{len(stems)} distinct stems, no cross-file duplicates'
    if not dups else f'dups: {dups[:6]}')
d_fail = 1 if dups else 0

# ------------------------------------------------- 7. exam mark consistency

def exam_marks(text):
    """Return (total, [a, b, c]) parsed from the header, or None."""
    total = re.search(r'\*\*[^*]*?(\d+)\s*marks\*\*', text)
    parts = re.search(r'\((?:Section )?A\s*(\d+)\s*·\s*B\s*(\d+)\s*·\s*C\s*(\d+)\)',
                      text)
    if not (total and parts):
        return None
    a, b, c = (int(x) for x in parts.groups())
    return int(total.group(1)), [a, b, c]


mt = rd(os.path.join(A, 'exams', 'midterm-student.md'))
fn = rd(os.path.join(A, 'exams', 'final-student.md'))
mt_parsed, fn_parsed = exam_marks(mt), exam_marks(fn)
mt_ok = bool(mt_parsed and '90 minutes' in mt and
             sum(mt_parsed[1]) == mt_parsed[0] == 60)
fn_ok = bool(fn_parsed and '120 minutes' in fn and
             sum(fn_parsed[1]) == fn_parsed[0] == 70)
add('exam-consistency', 'PASS' if (mt_ok and fn_ok) else 'FAIL',
    f'midterm 90min/{mt_parsed} ; final 120min/{fn_parsed}'
    if (mt_ok and fn_ok) else f'midterm={mt_parsed} final={fn_parsed}')
e_fail = 0 if (mt_ok and fn_ok) else 1

# --------------------------------------- 8. weighting caveat & honesty marks
rdme = rd(os.path.join(A, 'README.md'))
caveat = ('proposed plan' in rdme and 'not' in rdme and
          'confirmed institutional policy' in rdme)
mc_dc = rd(os.path.join(A, 'marking-guide.md'))
mc_ok = '[MC]' in mc_dc and '[DC]' in mc_dc
add('weighting-caveat', 'PASS' if (caveat and mc_ok) else 'FAIL',
    'proposed-plan caveat + [MC]/[DC] verification convention present'
    if (caveat and mc_ok) else f'readme={caveat} marking-guide={mc_ok}')
c_fail = 0 if (caveat and mc_ok) else 1

# ------------------------------------------------ 9. numeric verification gate
proc = subprocess.run(
    [sys.executable, os.path.join(ROOT, 'tools', 'scripts',
                                  'verify_assessment_numbers.py')],
    capture_output=True, text=True)
tail = (proc.stdout or '').strip().splitlines()[-1] if proc.stdout else 'no output'
add('numeric-verification', 'PASS' if proc.returncode == 0 else 'FAIL', tail)
n_fail = proc.returncode != 0

# ---------------------------------------------------- 10. links resolve inside
link_re = re.compile(r'\]\(([^)#]+?)(?:#[^)]*)?\)')
broken = []
for dirpath, _, files in os.walk(A):
    for fn in files:
        if not fn.endswith('.md'):
            continue
        p = os.path.join(dirpath, fn)
        for m in link_re.finditer(rd(p)):
            target = m.group(1)
            if target.startswith(('http://', 'https://', 'mailto:')):
                continue
            resolved = os.path.normpath(os.path.join(dirpath, target))
            if not os.path.exists(resolved):
                broken.append((fn, target))
add('links-resolve', 'PASS' if not broken else 'FAIL',
    'all relative links inside assessments/ resolve'
    if not broken else f'broken: {broken[:8]}')
l_fail = 1 if broken else 0

# ------------------------------------ 11. integrity & rubric required content
ai = rd(os.path.join(A, 'academic-integrity.md'))
ai_ok = ('Collaboration matrix' in ai and 'reproducibility' in ai.lower()
         and 'Generative AI' in ai)
pr = rd(os.path.join(A, 'rubrics', 'practical-work-rubric.md'))
cp = rd(os.path.join(A, 'rubrics', 'capstone-rubric.md'))
rub_ok = ('Correct results' in pr and 'Evidence reproducibility' in pr and
          'Defense' in cp and 'Peer contribution' in cp)
add('integrity-rubrics', 'PASS' if (ai_ok and rub_ok) else 'FAIL',
    'integrity matrix/rules + practical & capstone rubric dimensions present'
    if (ai_ok and rub_ok) else f'integrity={ai_ok} rubrics={rub_ok}')
i_fail = 0 if (ai_ok and rub_ok) else 1

# ------------------------------ 12. quiz-window reconciliation note survives
w_note = ('W04' in rdme and 'reconcil' in rdme.lower())
add('quiz-window-note', 'PASS' if w_note else 'WARN',
    'README flags the W04/W07/W10/W13 vs W04/W12 discrepancy'
    if w_note else 'README missing the quiz-window reconciliation note')

fails = inv_fail + q_fail + r_fail + b_fail + t_fail + d_fail + e_fail + c_fail \
    + n_fail + l_fail + i_fail
warns = 1 if results[-1][1] == 'WARN' else 0

print('=' * 74)
for check, status, detail in results:
    mark = {'PASS': '[PASS]', 'FAIL': '[FAIL]', 'WARN': '[WARN]'}[status]
    print(f'{mark} {check:<24} {detail}')
print('=' * 74)
p = sum(1 for r in results if r[1] == 'PASS')
print(f'Total: {p} PASS / {warns} WARN / {fails} FAIL')
sys.exit(1 if fails else 0)
