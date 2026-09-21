#!/usr/bin/env python3
"""Validate every relative Markdown link in README.md (and optionally other files).

Checks that each relative link target exists on disk (file or directory; a
directory link must contain README.md or index.md to be an index link).
Absolute http(s) URLs are only counted, not fetched (live checks are done
separately with curl). Fragment part (#...) is stripped before the path check,
but directory-index fragment targets like dir/#anchor are validated against
dir/README.md / dir/index.md.

Run from the repository root:  python tools/scripts/check_readme_links.py [files...]
Exit 0 = all good; 1 = at least one broken/ambiguous link.
Standard library only.
"""
import os
import re
import sys

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def slugify(heading):
    """Approximate GitHub's heading-anchor slugger."""
    s = heading.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)   # drop punctuation (keeps letters/digits/_/-)
    s = s.replace(" ", "-")
    return s


def headings(text):
    out = set()
    for line in text.splitlines():
        m = re.match(r"\s*#{1,6}\s+(.*?)(?:\s+#+\s*)?$", line)
        if m:
            out.add(slugify(m.group(1)))
    return out


def resolve(base_dir, target):
    """Return (status, detail) for target relative to base_dir.

    status: ok | missing | no-index | special
    """
    path, frag = target.split("#", 1) if "#" in target else (target, "")
    if path == "":
        # pure fragment on the same page — fine
        return ("ok", "same-page fragment")
    if path.startswith("/"):
        return ("missing", "repo-root-absolute path (breaks under /Computer-Networks/ on Pages)")
    if path.lower().startswith(("http://", "https://")):
        return ("special", "external URL")
    if path.startswith("mailto:"):
        return ("special", "mailto")
    full = os.path.normpath(os.path.join(base_dir, path))
    if not os.path.exists(full):
        return ("missing", f"target does not exist: {full}")
    if os.path.isdir(full):
        # A directory link renders as a GitHub file listing — valid if non-empty;
        # if it has an index file, validate any fragment against that index.
        entries = [e for e in os.listdir(full) if not e.startswith(".")]
        if not entries:
            return ("no-index", "directory is empty")
        idx = None
        for cand in ("README.md", "index.md"):
            if os.path.isfile(os.path.join(full, cand)):
                idx = os.path.join(full, cand)
                break
        if frag and idx:
            hs = headings(open(idx, encoding="utf-8", errors="replace").read())
            if frag not in hs:
                return ("missing", f"fragment #{frag} not a heading slug in {idx}")
        elif frag:
            return ("no-index", "fragment points at a listing-only directory")
        return ("ok", "directory listing" + (" + index" if idx else ""))
    # file target: if it has a fragment, check it against the file's heading slugs
    if frag:
        hs = headings(open(full, encoding="utf-8", errors="replace").read())
        if frag not in hs:
            return ("missing", f"fragment #{frag} not a heading slug in {full}")
    return ("ok", "file")


def main():
    files = sys.argv[1:] or ["README.md"]
    bad = 0
    total = external = 0
    for f in files:
        if not os.path.isfile(f):
            print(f"MISSING FILE: {f}")
            bad += 1
            continue
        base = os.path.dirname(f) or "."
        text = open(f, encoding="utf-8", errors="replace").read()
        for m in LINK.finditer(text):
            target = m.group(1)
            status, detail = resolve(base, target)
            if status == "special":
                external += 1
                continue
            total += 1
            if status != "ok":
                bad += 1
                print(f"BROKEN in {f}: ({target}) — {detail}")
            elif detail == "directory listing":
                print(f"note (GitHub listing): ({target})")
    print(f"\nrelative/internal links checked: {total}  external URLs: {external}  broken: {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
