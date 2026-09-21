# LAB-11 — Reliable Transport over UDP: Implementation & Evaluation

| Field | Value |
|---|---|
| Anchor lectures | L20 (assign), W12 demo slot (per schedule/assessment map) |
| CLOs | CLO4, CLO5, CLO6 |
| Assessment | Implementation + demo half of the 10% project (with LAB-10's spec) |
| Mode / duration | Pairs; out-of-class build + in-session demo (10 min per pair) |
| Environment | Namespaces + netem (reuse LAB-09's topology); Python 3.10+; `tcpdump` for evidence |

## Learning outcomes
1. Implement your LAB-10 specification (chunk format, ACK/retry, termination) in Python
   over UDP — and log every deviation from the spec as an amendment.
2. Run the LAB-10 evaluation matrix for real: same loss/reorder/delay settings, measured
   time and retransmit counts.
3. Compare predictions vs reality and explain every gap with a mechanism (timeout too
   long? ACK path loss? reorder panic?).
4. Demonstrate the protocol live, including its failure path (kill the server mid-transfer
   on purpose — recovery *is* the deliverable).

## Pre-lab (before coding)
1. Re-read your spec's guarantee sentence: what exact command sequence will *prove* it?
2. Which netem setting tests the reordering rung? (From LAB-09 T4.)
3. What does your receiver do with chunk seq=n+1 while seq=n is still missing — buffer,
   drop, or nack? (Spec must already answer this; code must match it.)

## Tasks

### T1 — Implement to spec (out of class)
Skeleton provided (`lab11-skeleton.py` — sender loop with timers, receiver with dedup
stubs); graded work is the spec's logic, not boilerplate. Deviations → `SPEC-AMENDMENTS.md`
(one line each: what, why). Pair with silent deviations loses reproducibility points.

### T2 — Verification first (in session, 15 min)
Run your guarantee-sentence proof at the *easy* settings (0% loss): byte-identical file
(`sha256sum` both ends), zero retransmits expected. **This gate must pass before the
demo** — debugging basic paths during the demo slot is the classic failure.

### T3 — The matrix, for real (25 min)
LAB-09 topology with the spec's settings: 0% / 2% / 5%+reorder, 1 MB file. Record wall
time, retransmit count (your own counter), and `sha256sum` after each run.
**Expected observation (shape, not numbers):** times rise and retransmit counts rise with
loss; reorder adds fast-retransmit-like behavior if you implemented dup-ack style
resends. Your numbers are yours — the report compares them with the LAB-10 matrix.

### T4 — Failure path demo (10 min prep)
Kill the receiver mid-transfer; show recovery (timeout → resend → completion) and the
*counts* from your logs. Then show the deadlock case from your spec's post-lab Q3 —
and why your design avoids it.

### T5 — The 10-minute demo (graded)
1 min guarantee sentence → 2 min T2 proof → 3 min T3 highlight (worst cell) →
2 min T4 recovery → 2 min questions (amendments, timers, termination defense).

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| Works at 0%, hangs at 2% | timer started per-chunk *after* send but never rearmed on resend | rearm on every resend; log timeouts to count them |
| File differs at 5%+reorder | dedup missing (late chunk overwrites newer data) | receiver must drop seq ≤ acked (spec said so; amendment if changed) |
| Throughput ~0 with window | you implemented stop-and-wait despite a windowed spec | implement the spec or amend it — graded on consistency |
| Demo machine lacks netem | environment not from setup guide | Route A/B/C all ship netem; run `check_lab_env.py` first |

## Post-lab questions (report + demo appendix)
1. Prediction-vs-reality table: each matrix cell, Δ time, Δ retransmits, one-line
   mechanism for the gap.
2. Which amendment did you log, and what design pressure forced it?
3. Your timeout value from the spec: did reality agree (too short → spurious resends;
   too long → slow recovery)? Cite your T4 log.

## Challenge (ungraded)
Implement the cumulative-ACK variant from LAB-10's challenge and repeat the 2% cell;
report which design survived ACK loss better and whether your LAB-10 prediction held.

## Accessibility / low-resource alternatives
- All-Python single machine works (`127.0.0.1` + `tc` on `lo` for impairment) — no VM
  needed for pairs without lab-room access; demo slot rules unchanged.
- Demo may be recorded video for students with approved accommodation ⚠ instructor
  approves case-by-case; live Q&A still required.
- Screen-reader friendly: all logs are text; no GUI dependency.

## Safety notes
Lab-internal only (syllabus-safety §3.1); synthetic files (no personal data, §3.4).
Demo failure injection targets your own receiver only.
