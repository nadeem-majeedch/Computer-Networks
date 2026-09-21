# Semester Calendar — Documentation & Maintenance Guide

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Companion pages | [Semester Calendar page](https://nadeem-majeedch.github.io/Computer-Networks/calendar/) · [`_calendar.yml` configuration](https://github.com/nadeem-majeedch/Computer-Networks/blob/main/site-src/_calendar.yml) · [`calendar_lib.py` engine](https://github.com/nadeem-majeedch/Computer-Networks/blob/main/tools/scripts/calendar_lib.py) |

## 1. How the calendar works

One configuration file drives the whole calendar. The engine
(`tools/scripts/calendar_lib.py`) reads `site-src/_calendar.yml`, walks the
configured teaching days from the semester start, assigns the 32 lectures in
master-schedule order (`docs/schedule-32-lectures.md` — titles and content are
never changed by the calendar), emits holiday rows, and resolves every
assessment milestone (`L16` → that lecture's computed date, `W10` → that
teaching week's first date). `tools/scripts/build_site_docs.py` renders the
result into the site's Semester Calendar page and writes `calendar.ics` /
`calendar.csv` next to it.

Nothing in the pipeline invents dates: until you configure them, the only
dates shown are those *derived* from `semester_start` plus the day-of-week
pattern.

## 2. Configuration reference (`site-src/_calendar.yml`)

| Field | Type | Effect |
|---|---|---|
| `semester_start` | date | Any configured lecture day in week 1 (a Monday in the default). Non-teaching start dates are normalized forward to the first teaching day. |
| `lecture_days` | list of `Mon…Sun` | Teaching slots per week. Two entries = 2 lectures/week (32 lectures / 16 weeks). |
| `lectures_per_week` | int (informational) | Must match `len(lecture_days)` for the 16-week plan; the engine derives weeks from the day walk, not this field. |
| `holidays` | list of dates | No-lecture dates. Rows appear as "**label** (no lecture)" and every later lecture shifts. |
| `holiday_labels` | date → text | Label for a holiday row. |
| `cancellations` | `Lxx` → text | Pre-known cancellation of a specific lecture (adds a note; pair with `makeups`). |
| `makeups` | `Lxx` → text | Where a cancelled lecture is made up (adds a note). |
| `assessment_dates` | field map | Overrides below; **empty = default**. `Lxx`/`Wnn` refs resolve to computed dates. |
| `lecture_notes` | `Lxx` → text | Extra per-lecture notes merged over the strategy-derived defaults. |

### `assessment_dates` fields and defaults

| Field | Default | Meaning |
|---|---|---|
| `quiz_windows` | *W4 and W12 per the syllabus calendar (reconciliation note)* | Graded quiz sessions (best 2 of 4). |
| `midterm_lecture` | `L16` | Lecture hosting the 90-minute midterm. |
| `subnetting_due` | `L16` | Subnetting problem set (5%). |
| `cs02_due` | `L16` | Case study CS-02 (LAN design + addressing plan). |
| `cs03_evidence` / `cs03_diagnosis` / `cs03_rca` | `L23` / `L26` / `L29` | CS-03 staged deliverables (evidence log, diagnosis, RCA report). |
| `transport_spec` / `transport_demo` | `L20` / `L24` | Reliable-transport project (LAB-10/11 pairs). |
| `capstone_design` / `capstone_demo` / `capstone_defense` | `W13` / `W15` / `L32` | CS-04 capstone stages (teams of 3–4). |
| `finals_note` | *finals week* | Free-text note for the final exam (no institutional date invented). |

The defaults come from `docs/assessment-strategy.md` §2–§3 and the syllabus
calendar; the standing W4/W7/W10/W13-vs-W4/W12 quiz-window discrepancy between
those two documents is carried through verbatim (see the reconciliation note
on the calendar page) until you resolve it.

## 3. Semester-planning workflow

1. Copy the university's academic calendar (teaching days, holidays, finals
   week) — **do not guess**.
2. Edit `site-src/_calendar.yml`: `semester_start`, `lecture_days`, `holidays`,
   `holiday_labels`, then `assessment_dates` if your dates differ from the
   defaults.
3. Validate: `python tools/scripts/calendar_lib.py --validate` → all checks
   must pass (21 date-calculation tests, including the holiday-shift
   invariant).
4. Regenerate: `python tools/scripts/build_site_docs.py`, then rebuild/redeploy
   the site (`mkdocs build --strict`).
5. Re-confirm the printed midterm/exam dates against the department's room and
   invigilation bookings — the engine moves *course* events, not university
   exam sessions.

### Mid-semester cancellation drill

Add the date to `holidays` (with a label) and rebuild. Every later lecture
shifts by one slot automatically; week numbering stays Monday-anchored; the
affected milestones re-resolve to the new dates. Re-run validation, then
announce the new dates. If a lecture must instead be *dropped* (not shifted),
remove it from the master schedule first — the calendar always schedules all
32.

## 4. Validation tests (what `--validate` proves)

| Group | Checks |
|---|---|
| Inputs | config loads with 2 lecture days; 32 titles parse from the master schedule |
| Placement | all 32 lectures placed exactly once in order; only on configured days; never on a holiday; dates strictly increasing; ≤ 20 teaching weeks |
| Weeks | numbering starts at 1 and never decreases; default plan = 2 lectures in each of 16 weeks; 16 anchors; W8 holds L15/L16 |
| Milestones | midterm placeholder resolves; milestone table builds with 8 rows; midterm milestone equals L16's date |
| Overrides | cancellations/makeups propagate to notes; title spot-check |
| Invariants | injected holiday preserves order and shifts the affected + later lectures while earlier lectures keep their dates; nothing lands on the holiday |

Exit code 0 = publishable; 1 = fix the configuration first.

## 5. Exports

| Artifact | Produced by | Consumed by |
|---|---|---|
| `site/calendar.ics` (32 all-day VEVENTs, CRLF) | generator; also `calendar_lib.py --export-ics FILE` | Outlook / Google / Apple Calendar import |
| `site/calendar.csv` (week, date, day, lecture, module, notes) | generator; also `--export-csv FILE` | Excel/Sheets planning sheets |
| Printed Semester Calendar page | browser print | course-outline appendix |

Exports are all-day events on purpose: lecture *hour* is institutional data
the course does not own.

## 6. Alignment guarantees

- Lecture numbers and titles come from the finalized
  `docs/schedule-32-lectures.md` — the calendar cannot drift from the outline
  (32 titles are a validation precondition).
- Module labels come from the same 8-module structure used across lectures,
  slides, review sets, and exams.
- Milestone defaults trace to `docs/assessment-strategy.md`; any override is
  visible in the config diff, so the published calendar and the graded plan
  cannot silently diverge.

## 7. Verification history

- `calendar_lib.py --validate`: **21/21 PASS** (2026-09-20).
- Exports machine-checked: 32 VEVENTs, strict CRLF; CSV = 33 rows, L01…L32.
- Full audit regression after integration: foundation 15/15 · lectures 14/14 ·
  labs 9/9 · case bank 10/10 · assessment 12/12 · site validation 26/26 ·
  `mkdocs build --strict` clean.
