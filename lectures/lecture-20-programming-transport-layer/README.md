# Lecture 20 — Programming the Transport Layer: Reliability over UDP

| Field | Value |
|---|---|
| Module | 4 — Transport Layer |
| Depends on | L17 (UDP), L18–L19 (TCP machinery you will rebuild) |
| CLOs addressed | **CLO5, CLO6** (primary) |
| Bloom level | C5–C6 |
| Assessment artifact | Project spec (graded milestone, due today) |
| Lab | LAB-10/11: reliable transport over UDP (design + implement; demo W12) |
| Readings | KR §3.4 (principles); instructor project brief (labs/) |
| Prerequisites | L17–L19; LAB-08 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · project brief (labs/) |

## Key questions
- You now know every mechanism TCP provides. Which do you *actually* need, and what
  does each cost?
- How do you design (not just code) a protocol: states, timers, and the failure cases?
- How will you *prove* your protocol works under loss — not just hope it does?

## What you should be able to do afterwards
- Decompose reliability into the ladder rungs and choose the subset for a goal.
- Write a protocol spec: header layout, states, timers, edge cases.
- Design an evaluation: loss/reordering/delay matrices with predicted outcomes.
- Start LAB-10/11 with a graded spec in hand.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md) · project brief

## Assessment reminder
The project spec is due at the END of this session (graded milestone, 10% instrument's
first stage). Bring L18/L19 worksheets — they contain the mechanisms you'll cite.

## Homework / preparation for next lecture
- Implement per your spec. Read KR §2.4 (DNS) — Module 5 begins.
