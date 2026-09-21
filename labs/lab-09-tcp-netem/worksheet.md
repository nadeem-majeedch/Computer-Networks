# LAB-09 Worksheet

Name: ________________  Date: ______  Environment table: ______

## Pre-lab
1. AIMD: increase rule ________________ ; loss rule ________________
2. Fixed cwnd, +50 ms RTT → throughput: ______________________
3. Why 1% loss hurts more than 1% retransmit bytes: ______________________

## T1 — Impairment verification
| Setting | ping RTT (avg) | Expected | Match? |
|---|---|---|---|
| none | | | |
| delay 50ms | | ~100 ms | |
| + rate 10mbit | | | |

## T2 — Throughput vs delay (3 runs each; median too)
| Impairment | R1 | R2 | R3 | Median | Implied window (median × RTT) |
|---|---|---|---|---|---|
| none | | | | | |
| 50 ms | | | | | |
| 100 ms | | | | | |

## T3 — Throughput vs loss
| Loss | R1 | R2 | R3 | Median | Retrans (ss -ti) |
|---|---|---|---|---|---|
| 0% (50 ms) | | | | | |
| 1% | | | | | |
| 3% | | | | | |

## T4 — Reordering caveat
Observed duplicate-ACK / fast-retransmit evidence: ______________________
Design implication for LAB-10/11 (two sentences in report): ______________________

## Post-lab (full answers in report)
1. Implied windows: constant or growing — and what limited you
2. Convex loss curve via AIMD
3. The faked signal + the better design
4. What netem rate is not (vs real bottleneck)
