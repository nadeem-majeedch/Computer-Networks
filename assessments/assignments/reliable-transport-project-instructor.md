# Reliable-Transport Project — Instructor Guide & Marking Scheme

| Field | Value |
|---|---|
| Access | Instructor only |
| Companion | Student brief · LAB-10/11 packages · [`../rubrics/practical-work-rubric.md`](../rubrics/practical-work-rubric.md) §3 (100-point grid, same weights) |
| ITI | Run the reference solution once before W10; keep the LAB-11 netem helper tested |

## Marking scheme (100 points → 10% course weight)

| Dimension | Pts | What full credit looks like |
|---|---|---|
| Correctness under loss | 40 | Transfer completes at 1% and 2% netem loss with measured (not asserted) results; retransmission actually fires under loss (capture/log evidence); no deadlock or duplicate-corruption bug |
| Protocol design quality | 25 | Segment layout coherent (seq space, flags); state machine correct incl. close; RTO value justified; window sized with BDP reasoning (bonus territory here) |
| Experiment interpretation | 20 | Throughput numbers for 0/1/2% reported as measured; limiting mechanism named *with evidence* (e.g., implied window = rate×RTT ≪ configured window → window-bound); limitations honest |
| Code clarity | 15 | Names/comments map to spec; no dead code; reproducible run instructions |

**Pair-splitting rule:** both members must answer two live questions at the demo (one
on design, one on results). Failure on both → cap that member's interpretation marks;
single failure → note and continue (explainability rule, integrity doc §1).

## Design-spec checkpoint (W10, formative)

Approve specs against four gates: seq/ACK layout · timer policy · close/teardown ·
test plan with *real* netem commands. Return within 1 week (strategy §6). Specs are
not graded but a spec missing a gate predicts demo failure — require revision before
W12.

## Common pitfalls (from protocol reasoning, flagged for the ITI run)

- Sequence numbers counted per *segment* vs per *byte* inconsistently between sender
  and receiver.
- Fixed RTO shorter than the netem 50 ms×2 path → spurious retransmit storms at 2%
  loss; fine as a design choice only if stated and its cost acknowledged.
- Window = 1 (stop-and-wait) with no pipeline: passes correctness, caps design marks
  unless the size rationale is explicit and honest.
- Reports quoting "expected" numbers instead of measured ones — reproducibility rule:
  zero on interpretation until real outputs appear.

## Demo logistics

Two pairs per 2-hour lab block (10 min each + setup): one loss setting drawn live
(1% or 2%), file supplied by the instructor, capture on the netem router optional as
tie-breaker evidence. Record marks the same day.
