# Lecture 29 — Worksheet (GA-29) & Exit Ticket

Name: ________________  Date: ______  Pair: ________________

## Part A — Percentile arithmetic (5 min)
RTT set (ms): 10, 12, 12, 14, 18, 20, 25, 60, 110, 150
1. Mean: ________
2. p50: ________  3. p95: ________
4. In one sentence: why doesn't the mean describe the user's experience?

## Part B — GA-29 dashboard build (30 min)
5. Active probe results (fill from your run): ping p95 = ________ ms; HTTP
   check success % = ________
6. Passive counters (before/after the staged fault): tx_errors ________ /
   ________; retransmissions ________ / ________
7. Dashboard rows — during the fault window, record:
   | Question | Your row | Value during fault |
   |---|---|---|
   | Is the service up? | | |
   | How slow? (p95) | | |
   | Errors? | | |
8. Your alert threshold + one-sentence defense: ________

## Exit ticket (3 items)
1. Ping-up but users fail: the instrument that catches it: ________
2. Active vs passive: one probe, one counter: ________
3. One thing a 5-minute counter can hide: ________
