# LAB-14 Worksheet

Names (pair): ________________  ______  Date: ______  Environment table: ______

## Pre-lab
1. Polling: ______________________ streaming: ______________________
2. ifInOctets counts ______ ; deltas needed because: ______________________
3. p95 vs average: ______________________

## T1 — Baseline
Poll interval: ____ s ; samples: ____ ; p50 RTT ____ ms ; p95 RTT ____ ms
Throughput estimate (delta-derived): ______ — chart attached ☐

## T2 — Flow table (top 3)
| src | dst | bytes | note |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

## T3 — Fault signatures (one row per injected fault)
| Fault | First metric to move | Latency to detect (polls) | Signature |
|---|---|---|---|
| (a) delay spike | | | |
| (b) policy drop | | | |
| (c) link down | | | |

Blind-detection timestamps: detection at t=____ (dashboard) — first probe at t=____

## T4 — RCA skeleton (full RCA in report)
Symptom (metric + time): ______________________
Hypotheses ranked (2+, cheapest test first): ______________________
Evidence: ______________________ Cause: ______________________
Fix + verification: ______________________

## Post-lab (full answers in report)
1. Signatures + detection latency per fault
2. Why deltas, not raw counters
3. The losing hypothesis and its kill evidence
4. What the dashboard cannot tell you + the instrument that would
