# Lecture 01 — Worksheet & Exit Ticket

Name: ________________  Date: ______  (Submit at end of lecture; graded for participation.)

## Part A — Delay sorting (pairs, 10 min)

For each scenario, name the **dominant** delay component (processing / queueing /
transmission / propagation) or other listed concept, and one reason.

| # | Scenario | Dominant component | Why |
|---|---|---|---|
| 1 | Page loads slowly on a geostationary-satellite link | | |
| 2 | Campus Netflix buffers at 21:00 while lunchtime was smooth | | |
| 3 | Online-game ping spikes only when a big download runs | | |
| 4 | Copying a file between two data centres in different cities | | |
| 5 | Speed test: 500 Mbps down, but "loaded latency" 80 ms | | |
| 6 | Local file server copy faster than expected; other building's is not | | |

## Part B — Calculations (pairs, 12 min)

Show your work. State units. Propagation speed s = 2×10⁸ m/s.

1. Transmission delay of a 2,400-byte packet on a 1 Gbps link.
2. One-way propagation delay over 800 km of fibre.
3. Max achievable throughput: your access link is 50 Mbps; every other link on the path is
   1 Gbps. Why?
4. A 1,500-byte packet crosses three store-and-forward links of 10 Mbps each (ignore
   propagation/queueing). Approximate end-to-end transmission delay (KR approximation:
   N × L/R).
5. Link 100 Mbps; average packet 1,000 B; arrival rate 10,000 packets/s. Compute traffic
   intensity ρ = La/R and classify the queueing regime.

## Part C — Predict-observe (before the Wireshark demo)

1. Write your guess: how many packets does loading one small web page take? ______
2. After the demo: what surprised you most in the capture?

## Exit ticket (3 items, individual)

1. The four delay components are: __________, __________, __________, __________.
   Which one does a *longer distance* change? ________
2. In one sentence: bandwidth vs throughput.
3. One thing from the Wireshark tour you want explained later:
