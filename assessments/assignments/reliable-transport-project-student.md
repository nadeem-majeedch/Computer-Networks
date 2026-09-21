# Reliable-Transport Project (LAB-10/11) — Student Brief

| Field | Value |
|---|---|
| Instrument | Pair project · **10% of course weight (proposed plan)** — see [`../README.md`](../README.md) §4 |
| Milestones | Design spec due W10 · working demo (in-lab, 10 min) W12 |
| Rubric inside | Correctness under loss 40% · protocol design quality 25% · experiment interpretation 20% · code clarity 15% — full grid in [`../rubrics/practical-work-rubric.md`](../rubrics/practical-work-rubric.md) §3 |
| Integrity | Pair instrument ([`../academic-integrity.md`](../academic-integrity.md) §1): both members explain any part; AI-generated code not permitted |

## Task

Build a **reliability layer over UDP** in Python (standard library only) that
transfers a file of ≥ 1 MB between two namespace endpoints of the course lab stack,
with:

1. **Sequencing** — per-segment sequence numbers (your layout, documented).
2. **Acknowledgment** — at least cumulative ACKs; selective ACKs = design bonus.
3. **Timeout/retransmit** — an RTO you compute (fixed is acceptable; adaptive =
   bonus), with a stated value and reasoning.
4. **Verification under loss** — the LAB-11 netem profile (1%, then 2%) run by *you*,
   with real outputs in the report.

Bonus (design quality, +design marks): sliding window with a stated size rationale
(≥ 2× BDP of the test path, or a documented reason for less).

## Deliverables

| Artifact | Due | Notes |
|---|---|---|
| **Design spec** (≤ 4 pages) | W10 | Segment layout, state machine, timers, window plan, *test plan* |
| **Implementation + report** | W12 (demo) | Code + measured results + honest interpretation |
| **10-minute demo** | W12 | Both members present; live run under one loss setting |

## Report requirements (interpretation is graded, not just numbers)

- Environment block: commands used to build the netem profile (reproducibility rule).
- Throughput for 0%, 1%, 2% loss — *your measured numbers*, clearly labeled.
- One paragraph: which mechanism limited your throughput (RTO policy vs window) and
  the evidence.
- Known limitations — honest ones score; omissions found in the demo cost marks.

## Environment

Per [`../../labs/lab-10-reliable-design/README.md`](../../labs/lab-10-reliable-design/README.md)
and LAB-11: course VM/namespace stack, Python 3 standard library only. No external
networks. Offline-capture alternative exists for students without lab hardware —
agree it with the instructor in week 9.
