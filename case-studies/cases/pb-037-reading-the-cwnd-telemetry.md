# PB-037 — Reading the cwnd Telemetry (L19, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L19 — TCP Flow & Congestion Control |
| CLOs | CLO5 (window/congestion arithmetic), CLO2 (slow start vs congestion avoidance) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Calculation · Topic: Network performance (TCP) |
| Evidence policy | Synthetic transfer log, labeled; arithmetic desk-checked (MSS = 1460 B, RTT = 50 ms) |

---

## Student version

### Scenario
The analytics team instrumented one backup flow (unusual, but the sender logs its
congestion window each RTT). The link is otherwise idle.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (MSS = 1460 B; RTT = 50 ms):**

```
RTT#   1    2    3    4    5    6    7    8    9    10   11
cwnd   1    2    4    8    16   17   18   19   20   21   (loss during this RTT at 22)
Log note: "loss detected via 3 duplicate ACKs during RTT 11"
Post-loss telemetry:  ssthresh = 11, cwnd = 11 (RTT 12)
```

### Problem statement
Classify each growth phase, compute the bytes delivered per RTT and the instantaneous
throughput just before the loss, reconstruct the loss response arithmetic, and compute
the RTTs needed to rebuild cwnd to 22.

### Evidence pack
The labeled synthetic log. Conventions (state them): cwnd counted in MSS; slow start
doubles per RTT until ssthresh; congestion avoidance adds 1 MSS per RTT; 3-dup-ACK
loss → ssthresh = cwnd/2, cwnd = ssthresh (fast-recovery shorthand ⚠ Reno-style).

### Constraints
- Show the phase boundary (where doubling stops and +1 begins) explicitly.
- Throughput = cwnd × MSS × 8 ÷ RTT — show units.
- Rebuild count must start from the post-loss value.

### Student questions
1. Which RTTs are slow start, which are congestion avoidance? Where is the boundary
   and what set it?
2. Bytes in flight during RTT 10, and instantaneous throughput at that cwnd.
3. Reconstruct the loss response: pre-loss cwnd, new ssthresh, new cwnd — show the
   arithmetic. How would the answer differ if the loss had been a *timeout* instead?
4. How many RTTs (and seconds) to rebuild from the post-loss cwnd back to 22? What
   assumption does that count make?

### Expected learning outcomes
- Distinguish exponential (SS) and linear (CA) growth and locate the boundary.
- Convert window size to throughput with unit discipline.
- Apply Reno-style loss response and contrast timeout behavior.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Doubling while cwnd < ssthresh; then the growth becomes +1 per RTT. Which RTT is
   the hinge?"
2. "The loss response has two numbers: where the *target* (ssthresh) lands and where
   the *window* lands. A timeout sends them to different places than 3 dup-ACKs do."

### Solution
1. Slow start: RTTs 1–5 (1→2→4→8→16, doubling); congestion avoidance: RTT 6 onward
   (+1 per RTT: 17, 18, …). Boundary set by ssthresh = 16 (reached at RTT 5's cwnd).
2. RTT 10: cwnd = 21 MSS → 21 × 1460 = 30,660 B in flight. Throughput = 30,660 B × 8
   ÷ 0.05 s = 245,280 bits ÷ 0.05 = **4.9 Mb/s**.
3. Pre-loss cwnd = 22 (loss during RTT 11). 3-dup-ACK (Reno-style): ssthresh =
   ⌊22/2⌋ = **11**; cwnd resets to **11** (fast recovery collapses the window to half,
   not to one). Timeout instead: ssthresh = 11 as well, but **cwnd = 1** and slow
   start restarts — recovery from 1→11 takes ~4 RTTs of doubling before CA, far
   slower. The log's note (3 dup-ACKs) is what makes cwnd=11 (not 1) the correct read.
4. From cwnd = 11 to 22 in CA (+1/RTT): **11 RTTs** = 11 × 50 ms = **0.55 s**.
   Assumption: no further loss during rebuild (an idle link makes this reasonable —
   the log's context), and CA's +1/RTT shorthand (real implementations scale AIMD ⚠
   but the teaching model is exact here).

### Reasoning process
Facts: cwnd series, loss type, post-loss values. Model: SS doubling → CA linear;
loss-response fork (dup-ACK vs timeout). Compute per-RTT bytes → throughput; rebuild
time from post-loss state. Assumptions: idle link, model shorthand — both stated.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| Doubling through RTT 6 (cwnd 32) | ssthresh = 16 stops doubling at 16; ignoring ssthresh is the classic error |
| Throughput = cwnd × MSS ÷ RTT | Forgets ×8 (bytes→bits) — off by 8× |
| Post-loss cwnd = 1 | That's the timeout response; the log says 3 dup-ACKs → half, not collapse |
| Rebuild "9 RTTs" | Counts from 13; the window resumes at 11 — count from the actual post-loss value |

### Extension question
Two flows share this now-idle link, both in CA at cwnd = 20, and one packet from *each*
flow is lost in the same RTT. Sketch each flow's cwnd for the next 4 RTTs and explain
why AIMD converges to sharing — and what breaks the fairness if one flow's RTT is
10 ms instead of 50 ms. (Both halve to 10, then climb in parallel — equal-step CA
preserves equality. A 10 ms-RTT flow gains cwnd 5× faster in wall-clock time ⇒
throughput ≈ proportional to 1/RTT; classic RTT-unfairness.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Phase boundary tied to ssthresh; 4.9 Mb/s with unit discipline; dup-ACK vs timeout fork explicit; rebuild count + assumptions |
| 3 Proficient | Arithmetic correct; one convention misapplied |
| 2 Developing | Treats all growth as doubling or all as linear |
| 1 Beginning | "TCP slows down after loss" only |

### References
- PD §3.6/3.7 (congestion control: slow start, AIMD) ⚠ verify section mapping
- Kurose & Ross §3.6.2–3.7.1 (TCP congestion control essentials)
