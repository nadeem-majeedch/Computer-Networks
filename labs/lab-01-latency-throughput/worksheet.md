# LAB-01 Worksheet

Name: ________________  Date: ______  Environment (paste `check_lab_env.py` table): ______

## Pre-lab (before session)
1. Transmission-delay formula: ________
2. Estimates: RTT→gateway ____ ms; RTT→example.com ____ ms; VM→VM TCP ____ Mbit/s
3. Why 20 pings beat 1 ping: ______________________________________________

## T1 — Baseline (record from `ping -c 20`)
| Target | min | avg | max | mdev | traceroute hops |
|---|---|---|---|---|---|
| gateway | | | | | — |
| example.com | | | | | |

Which delay component dominates the internet path? ____________ Evidence: ____________

## T2 — Loaded latency
| Phase | avg RTT | mdev |
|---|---|---|
| before load | | |
| during iperf3 | | |

Growth = ______ ms. Explanation (which queue, where): ______________________

## T3 — Throughput (3 runs each; record all)
| Test | Run 1 | Run 2 | Run 3 | Units |
|---|---|---|---|---|
| TCP | | | | Mbit/s |
| UDP -b 100M (loss%) | | | | % |
| UDP -b 0 (observed rate) | | | | Mbit/s |

## T4 — Wire check
Handshake order seen: ______ → ______ → ______ . Data flows one-way / both ways? ______

## Post-lab (full answers in report)
1. Dominant delay per path + citation of your numbers
2. Queue-length estimate with stated assumptions
3. Window ≈ throughput × RTT arithmetic; `ss -ti` comparison if captured
4. One thing your measurements cannot prove: ______________________
