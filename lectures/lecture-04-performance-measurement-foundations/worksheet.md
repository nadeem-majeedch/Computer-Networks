# Lecture 04 — Worksheet & Exit Ticket (LAB-01 kickoff)

Name: ________________  Date: ______  Pair: ________________

## Part A — Estimates BEFORE measuring (pairs, 8 min)
Write your estimate **and the reasoning behind it** before touching any tool.
Leave the "Measured" column blank until LAB-01 runs.

1. VM → gateway: estimated RTT = ________ ms. Reasoning: ______________________
2. VM → example.com: estimated RTT = ________ ms. Reasoning: ______________________
3. VM → VM (same physical host): estimated TCP throughput = ________ Mbps. Reasoning: ______
4. VM → VM while iperf3 runs in the background: estimated loaded RTT = ________ ms. Why does it change? ______

After the lab, record measurements and explain every deviation > 25%:

| # | Path & metric | Measured | Deviation & why |
|---|---|---|---|
| 1 | RTT to gateway (ms) | | |
| 2 | RTT to example.com (ms) | | |
| 3 | TCP throughput VM→VM (Mbps) | | |
| 4 | Loaded RTT during iperf3 (ms) | | |

## Part B — Output diagnosis (pairs, 8 min)
Your instructor shows 4 real tool outputs (normal / lossy / rate-limited /
asymmetric). For each: what it proves, what it does **not** prove, and the next
tool you would run.

5. Output A — proves: ________________ does NOT prove: ________________ next: ______
6. Output B — proves: ________________ does NOT prove: ________________ next: ______
7. Output C — proves: ________________ does NOT prove: ________________ next: ______
8. Output D — proves: ________________ does NOT prove: ________________ next: ______

## Exit ticket (3 items)
1. ping / traceroute / iperf3 measure ______ / ______ / ______ respectively.
2. "Loaded latency" growth is mostly ________ delay.
3. One rule you will follow in every lab report from now on: ________
