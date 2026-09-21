# LAB-14 — Instructor Guide

## Setup (before session)
- Ship the poller scaffold (Python: loop `ip -s link`/`/proc/net/dev` deltas → CSV) and the
  flow-aggregator scaffold; test both on the teaching image (snmpd optional — the `/proc`
  path is the designed default).
- Prepare three fault scripts (delay spike, firewall drop, link down) so blind injection
  is one command; ⚠ confirm which pairs run blind order per session.

## Solutions / expected values
- **Pre-lab 1:** polling asks periodically; streaming pushes events (netflow-style).
- **Pre-lab 2:** octets on that interface; counters are cumulative — deltas per interval
  give rates.
- **Pre-lab 3:** p95 resists outlier-dilution; averages hide spikes.
- **T3 signatures:** (a) p95 jumps ~80 ms×2 within one poll; (b) throughput drops, blocked
  counters rise, RTT normal — the split points at policy, not path; (c) counter deltas go
  zero/absent — *absence* is the signature. Students must name which signature they saw.
- **T4:** ranked hypotheses: e.g., for (a): congestion vs misconfigured shaper vs app
  slowness — cheapest test first (ping during fault).

## Common failure modes
1. Pairs detect the fault in the injection terminal and "notice" it on the dashboard
   retroactively — insist the *first* notice is the dashboard (timestamp it).
2. Counters confused with rates (no deltas) — flat lines everywhere.
3. RCA reads like a story, not a method — rubric rewards ranked hypotheses + kill evidence.

## Grading notes
- Correct results (40): baseline chart + fault signatures table.
- Analysis (30): RCA quality (method, not prose) + post-lab 3's losing-hypothesis logic.
- Reproducibility (20): poller code + CSVs + capture files.
- Clarity (10): timeline presentation; timestamps consistent across artifacts.
