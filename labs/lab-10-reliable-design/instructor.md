# LAB-10 — Instructor Guide

## Setup (before session)
- Print the worksheet tables (or share the template). Schedule the red-team exchange:
  pairs A↔B swap specs at minute 60 — timing matters for the clinic pattern.
- Coordinate with LAB-09: pairs should bring their own T4 note on reorder.

## Solutions / expected values
- **Pre-lab 3:** stop-and-wait on 50 ms RTT ≈ 1 chunk per 50 ms → ~20 chunks/s; at 1 kB
  chunks that is 0.16 Mbit/s — painful against 10 Mbit/s. Windowed designs fix it.
- **T1:** accept any *testable* guarantee sentence; reject vague "reliable" claims.
  Ordering + dedup + ack/retry are the standard picks; congestion control usually
  dropped with a stated rationale (lab-only link) — that is fine if *stated*.
- **T2:** graded on internal consistency, not a canonical answer: header unambiguous
  (magic + fixed field sizes), timers justified from measurement, termination chosen
  and defended.
- **T3:** predictions must be *numbers* (time, retransmits) — LAB-11 grades the delta.
  Common mistake: assuming lossless ACKs (see README troubleshooting).
- **Deadlock question:** classic answers: both sides in WAIT on lost data+ACK (fixed by
  sender timeout), or receiver discarding late-but-valid chunks after FIN (fixed by
  quiet-period > max retransmit budget).

## Red-team mechanics
Each reviewing pair must produce exactly two questions; hardest wins recognition.
Typical killer questions: "what if the FIN chunk is lost?", "what if seq wraps?",
"what if the same chunk arrives twice *after* an ack?". Spec must be amended in the
appendix — an unchanged spec loses the review's points.

## Common failure modes
1. Specs that say "TCP but over UDP" without justifying each borrowed mechanism —
   bounce them back at the clinic stage, not at grading.
2. Missing termination rules (the red-team usually catches these — that is its job).
3. Matrix predictions with no numbers ("slower", "more retransmits") — a spec that
   cannot be compared in LAB-11 fails the milestone.

## Grading notes (spec = 10% project milestone, per assessment-strategy §3.5)
- Guarantee sentence + rungs (30) · mechanics completeness/consistency (30) ·
  matrix with numeric predictions (20) · red-team appendix (20).
- The spec is binding for LAB-11: implementation deviations must be logged as
  amendments, silently deviating specs lose reproducibility points in LAB-11.
