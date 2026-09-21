---
title: Semester Calendar
icon: material/calendar-month
search:
  boost: 0.5
---

# Semester Calendar

The calendar below is **generated** from the master schedule
([docs/schedule-32-lectures.md](docs/schedule-32-lectures.md)) by
`tools/scripts/build_site_docs.py`, using the semester configuration in
[`site-src/_calendar.yml`](https://github.com/nadeem-majeedch/Computer-Networks/blob/main/site-src/_calendar.yml). Change the configuration and rebuild
to re-plan a semester — the master schedule content itself never changes.

## Configuration

??? example "How to configure a semester"

    Edit `site-src/_calendar.yml`:

    ```yaml
    semester_start: 2026-09-14   # the Monday of week 1 (or any lecture day in week 1)
    lecture_days: [Mon, Wed]     # two teaching days per week
    lectures_per_week: 2
    holidays:                    # dates on which a lecture is cancelled
      - 2026-11-09
    holiday_labels:
      2026-11-09: University holiday
    cancellations: {}            # optional: pre-known cancellations by lecture number
    makeups: {}                  # optional: "2026-11-11": "moved to lab block"
    ```

    Then run `python tools/scripts/build_site_docs.py` and rebuild the site. The
    generator walks the configured lecture days, skips holidays, and assigns the
    32 lectures in schedule order — so a holiday simply shifts everything after
    it.

<div class="cn-calendar" markdown>

| Week | Date | Day | Lecture | Module | Notes |
|---|---|---|---|---|---|
<!-- CN_CALENDAR_ROWS -->

</div>

## Assessment milestones

Dates below are **computed** from the semester configuration via
`tools/scripts/calendar_lib.py` — `L16` means "the date lecture L16 lands on";
`W10` means "the week-of date of teaching week 10". Configure them in
`assessment_dates` inside `site-src/_calendar.yml` (empty field = strategy
default).

<!-- CN_MILESTONE_ROWS -->

## Export and printable schedule

- **Calendar apps (Outlook/Google/Apple):** download
  [calendar.ics](calendar.ics) — the 32 lectures as all-day events with module
  and assessment notes. Import into a secondary calendar; all-day form because
  the university's hour grid is not course data.
- **Spreadsheet (Excel/Sheets):** download [calendar.csv](calendar.csv).
- **Print:** use the browser's print function on this page — the calendar table
  and milestone list print cleanly (tables paginate; the date column stays
  aligned). For a one-page printable plan straight from the course sources,
  print [docs/schedule-32-lectures.md](docs/schedule-32-lectures.md) from its
  repository view.

## Instructor instructions

1. Open [site-src/_calendar.yml](https://github.com/nadeem-majeedch/Computer-Networks/blob/main/site-src/_calendar.yml).
2. Set `semester_start` (any lecture day of week 1), `lecture_days`, and
   `holidays`/`holiday_labels`. Do **not** invent institutional dates — copy
   them from the university's academic calendar.
3. Optionally fill `assessment_dates` (empty = strategy defaults; `L16`/`W10`
   references resolve to computed dates) and any `lecture_notes`.
4. Run `python tools/scripts/build_site_docs.py`, then rebuild/deploy the site.
5. Before publishing to students, run the date-calculation checks:
   `python tools/scripts/calendar_lib.py --validate` (21 checks must pass).

Mid-semester cancellations: add the date to `holidays` and rebuild — every
later lecture shifts automatically and the affected week's second slot absorbs
the displaced lecture (the console output lists the new midterm/exam dates to
re-confirm with the department).
