# Lecture Template

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Companions | [`schedule-32-lectures.md`](schedule-32-lectures.md) · [`repository-structure.md`](repository-structure.md) |

Every lecture folder is built from this template so students and instructors can navigate
any of the 32 lectures identically. A lecture folder is **complete** only when every
required section below is filled with real content — no unfinished "to-be-decided"
scaffolding is published.

> **Phase scope (current build):** the teaching-package phase delivers `README.md`,
> `notes.md`, and `worksheet.md` for every lecture, with demonstration commands embedded in
> `notes.md` §9. `slides.md` decks and standalone `demo/` scripts are a later authoring pass
> and remain required before delivery sign-off (tracked in the audit reports).

## 1. Folder layout

```
lectures/lecture-NN-short-name/
├── README.md        # REQUIRED — student-facing overview & index
├── notes.md         # REQUIRED — instructor teaching notes
├── slides.md        # REQUIRED — Marp-compatible slide source
├── worksheet.md     # REQUIRED only if the lecture has a GA/exit ticket
├── demo/            # REQUIRED if a live demo is planned — pre-verified configs/scripts
└── assets/          # OPTIONAL — lecture-specific traces/images
```

## 2. `README.md` (student-facing)

```markdown
# Lecture NN — <Title>

| Field | Value |
|---|---|
| Module | <Module name> |
| Depends on | L<NN>, L<NN> |
| CLOs addressed | CLO<n>, CLO<n> (primary in bold) |
| Bloom level | C<n>–C<n> |
| Assessment artifact | <exit ticket / worksheet / lab link> |
| Lab | <LAB-xx / GA-xx / none> |
| Readings | <KR/PD/T section refs, per syllabus map> |

## Key questions
- <Question 1 that this lecture answers>

## What you should be able to do afterwards
- <Concrete ability statements, aligned to the CLOs above>

## Materials
- [Slides](slides.md) · [Worksheet](worksheet.md) · [Notes are instructor-facing](notes.md)
- Traces: <links into assets/ or shared assets/traces/>

## Homework / preparation for next lecture
- <Reading + task>
```

## 3. `notes.md` (instructor-facing) — required sections

1. **Objectives hook** — the driving question and the failure story used to open.
2. **Minute plan** — the M&C segments for this specific lecture (concept/activity split per
   module), with what happens in each.
3. **Concept walkthrough** — the precise explanations, derivations, and numbers; includes
   the worked calculation steps on the whiteboard.
4. **Demo plan** — each demo: predicted-question, exact commands, expected output,
   rollback plan, and date last verified (⚠ every semester).
5. **Anticipated difficulties** — where students typically stumble; which misconception
   from the register ([`teaching-methodology.md`](teaching-methodology.md) §8) is targeted.
6. **GA/exit-ticket answer key** — complete worked answers.
7. **Timing fallbacks** — what to cut if behind (always an (enr) item, never a core item).

## 4. `slides.md` (Marp-compatible)

- Marp front-matter: `marp: true`, `theme: default`, `paginate: true`; 16:9;
  colorblind-safe palette; minimum 24pt body text.
- Slide budget: ~25–35 slides for a 120-minute lecture (~1 slide/3.5 min concept time).
- Every diagram slide must be understandable from alt text alone.
- Screenshots of tool output must carry the tool version and date captured.
- ⚠ VERIFY rendering after any Marp/theme update before publishing.

## 5. `worksheet.md` (GA/exit ticket)

- 2–3 exit-ticket items (recalability) + GA tasks (application) when scheduled.
- Every item states which CLO it rehearses.
- Answer key lives in `notes.md` §6, never in the student file.

## 6. Quality gates before a lecture folder is marked complete

- [ ] All required files present with real content
- [ ] Metadata table matches the master schedule row (title, CLOs, Bloom, artifact, lab)
- [ ] Demo verified on the current VM image (date recorded)
- [ ] Traces referenced exist and their description matches their content
- [ ] Cross-links (schedule row ↔ lecture folder, lab folder, case study) work
- [ ] Reviewed per [`contributing-instructor-review.md`](contributing-instructor-review.md)
      and stamped Reviewed/Approved
