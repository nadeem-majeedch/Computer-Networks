#!/usr/bin/env python3
"""Command-syntax verifier for the Computer Networks lab workbook.

Run from the repository root:  python tools/scripts/check_lab_syntax.py

Extracts every fenced code block tagged `bash` or `python` from labs/**/*.md
and checks it *syntactically only*:
  * bash blocks  -> `bash -n` (parse, never execute; needs bash on PATH)
  * python blocks -> ast.parse (stdlib)
This makes no claim that any command was *executed* or produced the listed
expected observations — that requires a lab VM and an instructor run-through.
Exit 0 = all blocks parse (or bash unavailable, noted); 1 = real syntax errors.
Standard library only.
"""

import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile

# <placeholder> left unquoted in a bash block parses as an input redirection —
# silent student trap. Quoted '<placeholder>' is the documented convention.
PLACEHOLDER = re.compile(r"(?<!['\"<])<([A-Za-z][A-Za-z0-9._ -]*?)>(?!['\">])")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LABS = os.path.join(ROOT, "labs")

FENCE = re.compile(r"^```([A-Za-z0-9_+-]*)[ \t]*$", re.M)

def fenced_blocks(text):
    """Yield (lang, code, start_line) for each fenced block; unterminated = error marker."""
    blocks = []
    matches = list(FENCE.finditer(text))
    i = 0
    while i < len(matches) - 1:
        opener, closer = matches[i], matches[i + 1]
        if closer.group(1) == "" and text[closer.start() - 1] != "\n":
            pass  # closing fence with no language tag; opener language governs
        lang = opener.group(1).lower()
        code = text[opener.end():closer.start()]
        start_line = text.count("\n", 0, opener.end()) + 1
        blocks.append((lang or "plain", code, start_line))
        i += 2
    if len(matches) % 2 == 1:
        last = matches[-1]
        line = text.count("\n", 0, last.start()) + 1
        blocks.append(("UNTERMINATED", "", line))
    return blocks

BASH_STATE = {"usable": None, "note": "", "path": "bash"}  # None = unprobed

def _bash_candidates():
    """Ordered candidate bash executables, deduplicated, case-insensitively."""
    cands = []
    env = os.environ.get("CNLAB_BASH")
    if env:
        cands.append(env)
    w = shutil.which("bash")
    if w:
        cands.append(w)
    if os.name == "nt":
        try:  # the PATH-first bash may be the WSL stub; `where` finds the rest
            out = subprocess.run(["cmd", "/c", "where", "bash"],
                                 capture_output=True, text=True, timeout=30).stdout
            cands += [ln.strip() for ln in out.splitlines() if ln.strip()]
        except (OSError, subprocess.SubprocessError):
            pass
    seen, uniq = set(), []
    for c in cands:
        if c.lower() not in seen:
            seen.add(c.lower())
            uniq.append(c)
    return uniq

def _probe_bash():
    """One-time probe: is any `bash` on this host a working interpreter?
    Windows ships a WSL bash.exe stub that fails when no distro is installed;
    without this probe its launcher errors would masquerade as syntax errors."""
    if os.name != "nt" and shutil.which("bash") is None:
        BASH_STATE.update(usable=False, note="bash not found on PATH")
        return
    for cand in _bash_candidates():
        try:
            r = subprocess.run([cand, "-c", "exit 0"], capture_output=True,
                               text=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            continue
        if r.returncode == 0:
            BASH_STATE.update(usable=True, note="", path=cand)
            return
    BASH_STATE.update(usable=False,
                      note="no working bash found (Windows WSL stub present but no "
                           "distro installed); set CNLAB_BASH to a real bash to force")

def bash_parse(code):
    """Return None if `bash -n` accepts the script, else the stderr text.
    Returns 'BASH_UNUSABLE' when the interpreter itself cannot run (skip)."""
    if BASH_STATE["usable"] is None:
        _probe_bash()
    if not BASH_STATE["usable"]:
        return "BASH_UNUSABLE"
    td = tempfile.mkdtemp(prefix="cnlab-syntax-")
    try:
        p = os.path.join(td, "snippet.sh")
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(code)
        # cwd stays OUTSIDE td: on Windows a child's cwd inside td blocks cleanup
        r = subprocess.run([BASH_STATE["path"], "-n", p], cwd=os.getcwd(),
                           capture_output=True, text=True, timeout=30)
        return None if r.returncode == 0 else (r.stderr or "bash -n failed").strip()
    finally:
        shutil.rmtree(td, ignore_errors=True)

def python_parse(code):
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        return f"line {e.lineno}: {e.msg}"

def placeholder_warns(code):
    """Count unquoted <placeholders> in a bash block (quoted ones are fine)."""
    return [m.group(1) for m in PLACEHOLDER.finditer(code)]

def main():
    targets = {"bash": bash_parse, "sh": bash_parse, "python": python_parse}
    results, errors, unterminated, warns = [], [], [], []
    for dirpath, _, files in sorted(os.walk(LABS)):
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, ROOT).replace("\\", "/")
            text = open(path, encoding="utf-8").read()
            for lang, code, line in fenced_blocks(text):
                if lang == "UNTERMINATED":
                    unterminated.append(f"{rel}:{line}")
                    continue
                if lang not in targets:
                    continue
                if lang in ("bash", "sh"):
                    ph = placeholder_warns(code)
                    if ph:
                        warns.append(f"{rel}:{line}  unquoted <{ph[0]}> "
                                     f"(+{max(0, len(ph) - 1)} more) parses as redirection")
                fail = targets[lang](code)
                nlines = len(code.rstrip("\n").splitlines())
                results.append((rel, line, lang, nlines, fail))
                if fail:
                    errors.append((rel, line, lang, fail))

    ok = [r for r in results if r[4] is None]
    skipped = [r for r in results if r[4] in ("NO_BASH", "BASH_UNUSABLE")]
    errors = [r for r in errors if r[3] not in ("NO_BASH", "BASH_UNUSABLE")]
    print("Command-syntax verification (labs/**/*.md, fenced bash/python blocks)")
    print("=" * 72)
    print(f"Blocks checked: {len(results)}   "
          f"bash: {sum(1 for r in results if r[2] in ('bash', 'sh'))}   "
          f"python: {sum(1 for r in results if r[2] == 'python')}")
    if not BASH_STATE["usable"] and BASH_STATE["note"]:
        print(f"[SKIP] bash unusable on this host: {BASH_STATE['note']}")
        print("       Bash blocks count as SKIP, not FAIL — this is an environment")
        print("       limitation, not a content error. Re-run on a Linux lab VM")
        print("       for full bash coverage.")
    if unterminated:
        print(f"[FAIL] Unterminated fences: {len(unterminated)}")
        for u in unterminated:
            print(f"       {u}")
    if skipped:
        print(f"[SKIP] bash unavailable -> {len(skipped)} bash block(s) unchecked "
              "(list: " + ", ".join(sorted({f'{r[0]}:{r[1]}' for r in skipped})) + ")")
    for rel, line, lang, nlines, fail in ok:
        print(f"[PASS] {rel}:{line}  ({lang}, {nlines} lines)")
    for rel, line, lang, fail in errors:
        print(f"[FAIL] {rel}:{line}  ({lang})  {fail}")
    for w in warns:
        print(f"[WARN] {w}")
    print("-" * 72)
    print(f"Syntax PASS: {len(ok)}   syntax FAIL: {len(errors)}   "
          f"SKIP(bash unavailable): {len(skipped)}   "
          f"unterminated fences: {len(unterminated)}   "
          f"placeholder WARNs: {len(warns)}")
    print("Scope note: syntax only. Semantic correctness (flags, file names,")
    print("privilege requirements) still requires the instructor run-through.")
    return 1 if (errors or unterminated) else 0

if __name__ == "__main__":
    sys.exit(main())
