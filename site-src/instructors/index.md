---
title: For Instructors
icon: material/account-group
---

# For Instructors

This area orients new instructors; it does not reproduce instructor-only
assessment keys. Those live in the course sources and are separated as follows:

| Material | Location | Separation |
|---|---|---|
| Assessment keys, exams, marking schemes | `assessments/exams/*-instructor.md`, `assessments/assignments/*-instructor.md`, key fences in quizzes/banks | Separate files / fenced "INSTRUCTOR KEY" sections — keep out of student-visible builds |
| Lab instructor guides & solutions | `labs/<lab>/instructor.md` | Separate file per lab |
| Case-bank hints & solutions | `case-studies/cases/*.md` (instructor sections) | Per-case fenced sections |
| Audit reports | `docs/audit-reports/` | Internal QA record |

!!! danger "Before publishing"

    If you build a student-visible site from this repository, verify that
    instructor files are excluded (see
    [docs/repository-structure.md](../docs/repository-structure.md)'s
    instructor-only table and the build notes in
    [docs-meta/github-pages-deployment-report.md](../site-reports/github-pages-deployment-report/)).
    The default public build **excludes** instructor-only material.

## Where to start

1. [Teaching methodology](../docs/teaching-methodology.md) — the course's approach
2. [Contributing & instructor review](../docs/contributing-instructor-review.md) — roles and the review workflow
3. [Lecture template](../docs/lecture-template.md) — how packages are structured
4. Audit reports under *Documents* in the navigation — what has been verified and
   what still requires an instructor solve-through (ITI items)

## Semester setup

- Configure the calendar: [Semester Calendar](../calendar.md) → `site-src/_calendar.yml`
- Verify flagged items: every ⚠ in the course sources (edition numbers, tool
  versions, deployment-guide figures) — collected per lecture in each `notes.md`
  prep checklist
- Confirm institutional policies: grade bands, AI use, integrity process (each
  flagged ⚠ in the assessment package)

## Key documents

- [docs/syllabus.md](../docs/syllabus.md) · [docs/schedule-32-lectures.md](../docs/schedule-32-lectures.md)
- [docs/assessment-strategy.md](../docs/assessment-strategy.md) · [docs/clo-mapping.md](../docs/clo-mapping.md)
- [docs/lab-strategy.md](../docs/lab-strategy.md) · [docs/case-study-strategy.md](../docs/case-study-strategy.md)
