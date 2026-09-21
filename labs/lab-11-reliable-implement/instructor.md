# LAB-11 — Instructor Guide

## Setup (before session)
- Demo day logistics: 10 min/pair slots (W12 per the schedule); a visible timer; students
  submit code + logs the night before so slot time goes to live behavior, not setup.
- Keep LAB-09's topology script handy for instant netem setup on the demo bench.
- ⚠ Verify skeleton runs on the teaching image the week before (it shares LAB-08's stack).

## Grading grid (with LAB-10 spec = the 10% project; assessment-strategy §3.5)
| Component | Points |
|---|---|
| T2 guarantee proof (sha256 match, clean gate) | 15 |
| T3 matrix execution + evidence (logs, counts) | 25 |
| Prediction-vs-reality analysis with mechanisms | 25 |
| T4 recovery demo incl. deadlock discussion | 20 |
| Spec fidelity (amendments logged, no silent drift) | 15 |

## Solutions / expected values
- **Pre-lab 3:** spec answer expected: buffer-or-drop is a *choice* — graded on spec/code
  match, not the choice itself.
- **T3 shapes:** 2% cell: retransmit counts ≈ 2% of chunks × (1 + repeat-loss factor);
  5%+reorder: the reorder cell usually shows the *largest* prediction error (students
  rarely predict reorder's dup-ack panic) — that gap is the best analysis in the report.
- **T4:** recovery must show: timeout fires → resend → ack → completion, with the count
  matching the spec's 3-attempt cap (or an amended one).

## Common failure modes
1. Silent spec deviation (windowed spec, stop-and-wait code) — the fidelity row exists
   exactly for this; catching it in Q&A is fine, catching it in the code review is points.
2. Demo debugging: pairs who skipped T2's gate burn their slot on a broken baseline —
   enforce the gate (T2 passes or the demo reschedules).
3. Timeout too short + lossy ACK path → res ACK storms; the log shows it — great T4/Q3
   discussion material.

## Recognition (ungraded)
Challenge (cumulative ACK) results feed the course's L20 examples next semester with
permission — credit in the demo slot.
