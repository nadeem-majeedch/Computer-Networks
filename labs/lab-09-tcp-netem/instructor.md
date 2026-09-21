# LAB-09 — Instructor Guide

## Setup (before session)
- ⚠ Verify `sch_netem` loads on the teaching kernel and that `iperf3 -C bbr` support exists
  only if you allow the challenge; otherwise tell students CUBIC is the reference.
- Pre-generate the accessibility CSVs by running the task matrix yourself (3 runs/point,
  medians) — these same numbers are your answer key. **You are generating real data here;
  do not present the CSVs to students as anything but "a real run from this image."**

## Solutions / expected values
- **Pre-lab 1:** increase additively (+1 MSS/RTT); loss → multiplicative decrease (×½ CUBIC).
- **Pre-lab 2:** throughput halves at fixed window.
- **Pre-lab 3:** each loss may cost a window halving + timeout stall; the *cost* of a loss
  is the lost window time, not the lost bytes.
- **T1:** RTT ≈ 100 ms with both qdiscs (each direction crosses one); ≈50 ms with only
  r2s — the one-sided case is itself a teaching moment (egress-only shaping).
- **T2:** implied window ≈ throughput × RTT grows toward the socket max until limited —
  students should notice which run was window-limited vs rate-limited.
- **T3:** 1% loss commonly collapses throughput to tens of percent of baseline; 3% lower
  still — convexity comes from timeout stalls compounding halvings.
- **T4:** duplicate-ACKs → fast retransmit fires without real loss; better design:
  reorder-tolerant signals (SACK-style selection, per-packet timers, not bare dup-ACK
  counts) — exactly the LAB-10/11 spec discussion.
- **Post-lab 4:** netem rate is a *token-bucket-ish shaper at egress*, not a competing
  sender: no queueing competition, no cross-traffic — students typically see perfectly
  smooth delays unlike a real bottleneck.

## Common failure modes
1. Impairing `r1s` instead of `r2s` (works for delay, confuses rate/loss placement).
2. Students graph single runs — require medians-of-3 or the report loses points.
3. `ss -ti` sampled after the run finishes (empty) — sample during; provide the command.

## Grading notes
- Correct results (40): the 3/2/3-run matrix + verification ping (T1).
- Analysis (30): implied-window computation + convexity argument + T4 design implication.
- Reproducibility (20): `tc` lines verbatim + CSVs/graphs; medians stated.
- Clarity (10): honest variance discussion.
