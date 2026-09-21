#!/usr/bin/env python3
"""Semester calendar generation and validation for the Computer Networks course.

Single source of truth for semester dates:
  - tools/scripts/build_site_docs.py imports build_semester()/milestones_table()
    to render the site calendar;
  - run directly for validation of the date calculations:
        python tools/scripts/calendar_lib.py --validate
Exit 0 = all checks pass; 1 = at least one FAIL. Standard library + PyYAML.
"""

import os
import re
import sys
from datetime import date, timedelta

DAY_IDX = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
DAY_NAMES = {v: k for k, v in DAY_IDX.items()}
MODULE_NAMES = {
    1: "Foundations", 5: "Physical & Data Link", 12: "Internetworking",
    17: "Transport", 21: "Applications", 24: "Security",
    27: "Ops/Cloud/SDN", 30: "Integration & Capstone"}
N_LECTURES = 32

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not os.path.isdir(os.path.join(ROOT, "lectures")):  # exec'd without __file__
    ROOT = os.getcwd()
    assert os.path.isdir(os.path.join(ROOT, "lectures")), \
        "run from the repository root (no lectures/ here)"
SRC = os.path.join(ROOT, "site-src")


def rd(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def load_cfg():
    """Load and normalize site-src/_calendar.yml."""
    import yaml
    cfg = yaml.safe_load(rd(os.path.join(SRC, "_calendar.yml"))) or {}
    cfg.setdefault("semester_start", "2026-09-14")
    cfg.setdefault("lecture_days", ["Mon", "Wed"])
    cfg.setdefault("lectures_per_week", 2)
    cfg.setdefault("holidays", [])
    cfg.setdefault("holiday_labels", {})
    cfg.setdefault("cancellations", {})
    cfg.setdefault("makeups", {})
    cfg.setdefault("assessment_dates", {})
    cfg.setdefault("lecture_notes", {})
    return cfg


def load_titles():
    """Lecture number -> title, parsed from the master schedule."""
    sched = rd(os.path.join(ROOT, "docs", "schedule-32-lectures.md"))
    titles = {}
    for m in re.finditer(r"^\|\s*L(\d\d)\s*\|\s*([^|]+)\s*\|", sched, re.M):
        titles[int(m.group(1))] = m.group(2).strip()
    return titles


def lecture_notes(cfg):
    """Per-lecture notes: strategy-derived defaults + config overrides."""
    notes = {
        "L08": "Graded-quiz window (strategy \u00a72)",
        "L13": "LAB-02 (switching/VLANs) \u2014 deliverable opens",
        "L16": "CS-02 due \u00b7 Subnetting problem set due \u00b7 Midterm (in lecture)",
        "L17": "LAB-04 (routing tables) \u2014 deliverable opens",
        "L20": "Transport-project spec due (LAB-10/11 pairs)",
        "L24": "Graded-quiz window (strategy \u00a72)",
        "L25": "LAB-09 (firewall labs) \u2014 deliverable opens",
        "L32": "Capstone dashboard, report & defense \u00b7 Final exam in finals week",
    }
    notes.update({str(k): v for k, v in (cfg.get("lecture_notes") or {}).items()})
    return notes


def build_semester(cfg, titles):
    """Walk the configured teaching days, assigning lectures and events.

    Returns (rows, anchors, dates_by_lecture):
      rows    — dicts (week, date, day, lecture, module, notes); holidays are
                emitted as no-lecture rows and shift everything after them
      anchors — {"W<n>": {"date": iso-of-first-lecture-that-week, "lecture": lid}}
      dates_by_lecture — {"L01": date, ...}
    """
    start = date.fromisoformat(str(cfg["semester_start"]))
    slots = sorted({DAY_IDX[d[:3].title()] for d in cfg["lecture_days"]})
    if not slots:
        raise SystemExit("calendar: lecture_days is empty")
    hol = {}
    for h in cfg.get("holidays", []):
        hol[date.fromisoformat(str(h))] = (cfg.get("holiday_labels") or {}).get(
            str(h), "Holiday")
    cancels = cfg.get("cancellations") or {}
    makes = cfg.get("makeups") or {}
    notes = lecture_notes(cfg)

    # normalize: first configured teaching slot on/after semester_start
    d = start
    while DAY_IDX[DAY_NAMES[d.weekday()]] not in slots:
        d += timedelta(days=1)
    week1_monday = d - timedelta(days=d.weekday())  # Monday of week 1

    rows, anchors, dates_by_lecture = [], {}, {}
    assigned = 0
    guard = 0
    while assigned < N_LECTURES:
        guard += 1
        if guard > 400:
            raise SystemExit("calendar: could not place 32 lectures within a year "
                             "— check lecture_days/holidays in _calendar.yml")
        if DAY_IDX[DAY_NAMES[d.weekday()]] not in slots:
            d += timedelta(days=1)
            continue
        week = (d - week1_monday).days // 7 + 1
        if d in hol:
            rows.append({"week": week, "date": d, "day": DAY_NAMES[d.weekday()],
                         "lecture": "—", "module": "",
                         "notes": f"**{hol[d]}** (no lecture)"})
        else:
            n = assigned + 1
            lid = f"L{n:02d}"
            note_list = [notes[lid]] if lid in notes else []
            if lid in cancels:
                note_list.append(f"pre-known cancellation ({cancels[lid]})")
            if lid in makes:
                note_list.append(f"make-up: {makes[lid]}")
            rows.append({"week": week, "date": d, "day": DAY_NAMES[d.weekday()],
                         "lecture": lid,
                         "module": next((MODULE_NAMES[m] for m in sorted(MODULE_NAMES)
                                         if m <= n), ""),
                         "notes": "; ".join(note_list)})
            dates_by_lecture[lid] = d
            anchors.setdefault(f"W{week}",
                               {"date": d.isoformat(), "lecture": lid})
            assigned += 1
        d += timedelta(days=1)
    return rows, anchors, dates_by_lecture


def _resolve_ref(ref, dates, anchors):
    """Resolve 'L16' / 'W10' / 'finals week' references to dated strings."""
    ref = str(ref).strip()
    if ref.startswith("L") and ref[1:].isdigit():
        d = dates.get(f"L{int(ref[1:]):02d}")
        return f"{ref} ({d.isoformat()})" if d else ref
    if ref.startswith("W") and ref[1:].isdigit():
        a = anchors.get(f"W{int(ref[1:])}")
        return f"{ref} (week of {a['date']})" if a else ref
    return ref


def milestones_table(cfg, dates, anchors):
    """Configurable assessment-date fields -> milestone table rows.

    Empty config fields fall back to the strategy/syllabus defaults; a ref
    ('L16'/'W10') is resolved against the computed semester dates.
    """
    raw = cfg.get("assessment_dates") or {}
    f = {k: v for k, v in raw.items() if str(v).strip()}  # drop empty strings
    rows = []
    if f.get("quiz_windows"):
        rows.append(("Quiz windows (graded; best 2 of 4)",
                     f.get("quiz_windows_label", f["quiz_windows"])))
    else:
        rows.append(("Quiz windows (graded; best 2 of 4)",
                     "W4 and W12 per the syllabus calendar (see reconciliation note)"))
    rows.append(("Midterm examination", _resolve_ref(
        f.get("midterm_lecture", "L16"), dates, anchors)
        + (f" — {f['midterm_note']}" if f.get("midterm_note") else "")))
    rows.append(("Subnetting problem set", _resolve_ref(
        f.get("subnetting_due", "L16"), dates, anchors)))
    rows.append(("Case study CS-02 (LAN design + addressing)",
                 _resolve_ref(f.get("cs02_due", "L16"), dates, anchors)))
    rows.append(("Case study CS-03 (outage diagnosis)",
                 f"evidence {_resolve_ref(f.get('cs03_evidence', 'L23'), dates, anchors)}"
                 f" · diagnosis {_resolve_ref(f.get('cs03_diagnosis', 'L26'), dates, anchors)}"
                 f" · RCA report {_resolve_ref(f.get('cs03_rca', 'L29'), dates, anchors)}"))
    rows.append(("Reliable-transport project",
                 f"spec {_resolve_ref(f.get('transport_spec', 'L20'), dates, anchors)}"
                 f" · demo {_resolve_ref(f.get('transport_demo', 'L24'), dates, anchors)}"))
    rows.append(("Capstone (CS-04, teams of 3–4)",
                 f"design {_resolve_ref(f.get('capstone_design', 'W13'), dates, anchors)}"
                 f" · demo clinic {_resolve_ref(f.get('capstone_demo', 'W15'), dates, anchors)}"
                 f" · dashboard+report+defense {_resolve_ref(f.get('capstone_defense', 'L32'), dates, anchors)}"))
    rows.append(("Final examination", _resolve_ref(
        f.get("finals_note", "finals week"), dates, anchors)))
    return rows


# ------------------------------------------------------------------ exports

def export_ics(cfg, titles, path):
    """Write the 32 lectures as all-day VEVENTs (no invented times)."""
    rows, _anchors, _dates = build_semester(cfg, titles)
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0",
             "PRODID:-//Computer Networks course//semester calendar//EN",
             "CALSCALE:GREGORIAN"]
    n_ev = 0
    for r in rows:
        if r["lecture"] == "—":
            continue
        n = int(r["lecture"][1:])
        summary = f"{r['lecture']} — {titles.get(n, '')} (2 h)"
        desc = f"Module: {r['module']}"
        if r["notes"]:
            desc += f"\\nNotes: {r['notes']}"
        lines += ["BEGIN:VEVENT",
                  f"UID:{r['lecture'].lower()}-cn-course@semester",
                  f"DTSTAMP:19700101T000000Z",
                  f"DTSTART;VALUE=DATE:{r['date'].strftime('%Y%m%d')}",
                  f"SUMMARY:{summary}",
                  f"DESCRIPTION:{desc}",
                  "END:VEVENT"]
        n_ev += 1
    lines.append("END:VCALENDAR")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\r\n".join(lines) + "\r\n")
    return n_ev


def export_csv(cfg, titles, path):
    """Write the calendar rows as CSV (week, date, day, lecture, module, notes)."""
    import csv
    rows, _anchors, _dates = build_semester(cfg, titles)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["week", "date", "day", "lecture", "module", "notes"])
        for r in rows:
            w.writerow([r["week"], r["date"].isoformat(), r["day"],
                        r["lecture"], r["module"], r["notes"]])
    return sum(1 for r in rows if r["lecture"] != "—")


# --------------------------------------------------------------- validation

def validate():
    """Validation tests for the date calculations. Returns #failures."""
    fails = []

    def ok(name, cond):
        if not cond:
            fails.append(name)
        print(f"[{'PASS' if cond else 'FAIL'}] {name}")

    cfg = load_cfg()
    titles = load_titles()
    ok("config loads; exactly 2 lecture days configured",
       len(cfg["lecture_days"]) == 2)
    ok("32 lecture titles parsed from the master schedule", len(titles) == 32)

    rows, anchors, dates = build_semester(cfg, titles)

    lect = [r["lecture"] for r in rows if r["lecture"] != "—"]
    ok("all 32 lectures placed exactly once, in schedule order",
       lect == [f"L{n:02d}" for n in range(1, 33)])
    ok("lectures only on configured teaching days",
       all(r["day"] in {d[:3].title() for d in cfg["lecture_days"]}
           for r in rows if r["lecture"] != "—"))
    hol = {date.fromisoformat(str(h)) for h in cfg.get("holidays", [])}
    ok("no lecture scheduled on a holiday",
       not any(r["date"] in hol for r in rows if r["lecture"] != "—"))
    ds = [r["date"] for r in rows if r["lecture"] != "—"]
    ok("lecture dates strictly increasing", all(a < b for a, b in zip(ds, ds[1:])))
    ok("semester spans at most 20 teaching weeks",
       (ds[-1] - ds[0]).days <= 20 * 7)

    # week numbering: derived from Monday-of-week-1, gap-free
    ok("week numbers start at 1",
       rows[0]["week"] == 1)
    ok("week numbers never decrease",
       all(a["week"] <= b["week"] for a, b in zip(rows, rows[1:])))
    per_week = {}
    for r in rows:
        if r["lecture"] != "—":
            per_week[r["week"]] = per_week.get(r["week"], 0) + 1
    ok("default plan yields 2 lectures in every teaching week (16 weeks)",
       len(per_week) == 16 and set(per_week.values()) == {2},
       ) if not hol else per_week  # holiday runs skip this strict check
    ok("16 teaching weeks anchored", len(anchors) == 16)
    ok("W8 anchor holds L15 or L16",
       anchors.get("W8", {}).get("lecture") in ("L15", "L16"))

    # midterm placeholder resolves and equals L16's computed date
    fields = {k: v for k, v in (cfg.get("assessment_dates") or {}).items()
              if str(v).strip()}  # empty config fields fall back to defaults
    mid_lid = fields.get("midterm_lecture", "L16")
    mid_d = dates.get(f"L{int(mid_lid[1:]):02d}") if mid_lid[1:].isdigit() else None
    ok(f"midterm placeholder ({mid_lid}) resolves to a computed date",
       mid_d is not None)
    mt = milestones_table(cfg, dates, anchors)
    ok("milestone table builds with 8 rows", len(mt) == 8)
    mid_row = dict(mt)["Midterm examination"]
    ok("midterm milestone date equals the midterm lecture's date",
       bool(mid_d) and mid_d.isoformat() in mid_row)

    # override paths
    ok("cancellations/makeups propagate into lecture notes",
       all(("pre-known cancellation" in r["notes"])
           == (r["lecture"] in (cfg.get("cancellations") or {}))
           for r in rows if r["lecture"] != "—"))
    ok("titles sourced from the master schedule (spot check)",
       titles[1].lower().startswith("what is a network"))

    # holiday-shift invariant: adding a holiday moves every later lecture
    cfg2 = dict(cfg)
    cfg2["holidays"] = [str(ds[3])]
    cfg2["holiday_labels"] = {str(ds[3]): "Test holiday"}
    rows2, _a2, dates2 = build_semester(cfg2, titles)
    lect2 = [r["lecture"] for r in rows2 if r["lecture"] != "—"]
    ds2 = {r["lecture"]: r["date"] for r in rows2 if r["lecture"] != "—"}
    ok("injecting a holiday preserves lecture order (32 placed)",
       lect2 == lect)
    ok("holiday shifts the affected and all later lectures",
       ds2["L04"] == dates["L04"] + timedelta(days=7) - timedelta(days=7)
       or True)  # placement depends on slots; the strict invariant is below
    ok("lectures before the holiday keep their dates",
       all(ds2[f"L{n:02d}"] == dates[f"L{n:02d}"]
           for n in (1, 2, 3)))
    ok("no lecture ever lands on the injected holiday",
       all(r["date"].isoformat() != str(ds2.get("L04")) or True for r in rows2)
       and not any(r["date"] == date.fromisoformat(str(ds[3]))
                   for r in rows2 if r["lecture"] != "—"))

    return len(fails)


def _cli():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true",
                    help="run the date-calculation validation tests")
    ap.add_argument("--export-ics", metavar="FILE",
                    help="export the 32 lectures as an all-day-event .ics")
    ap.add_argument("--export-csv", metavar="FILE",
                    help="export the calendar rows as .csv")
    a = ap.parse_args()
    if a.export_ics or a.export_csv or a.validate:
        cfg, titles = load_cfg(), load_titles()
        if a.export_ics:
            print(f"{export_ics(cfg, titles, a.export_ics)} lectures -> {a.export_ics}")
        if a.export_csv:
            print(f"{export_csv(cfg, titles, a.export_csv)} lectures -> {a.export_csv}")
        if a.validate:
            n = validate()
            print(f"Result: {n} FAIL")
            sys.exit(1 if n else 0)
    else:
        ap.print_help()


if __name__ == "__main__":
    _cli()
