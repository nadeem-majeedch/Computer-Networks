# PB-006 — The Backup That Outgrew Its Window (L04, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L04 — Performance, Measurement & Quality of Service |
| CLOs | CLO5 (window/RTT modeling), CLO6 (evaluate a mitigation) |
| In-class slot | Main activity; 20 min, pairs → plenary |
| Case type | Calculation + trade-off · Topic: Network performance |
| Evidence policy | Synthetic measurements, labeled; arithmetic desk-checked and internally consistent |

---

## Student version

### Scenario
Meridian's nightly data-science backup pushes a **100 GB dataset** from HQ-A to HQ-B
over the 1 Gb/s fiber. The dataset is growing and the backup window (ending at 06:00)
keeps slipping. Network ops proposes two "fixes" from a vendor and the platform team
proposes a third.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Link:              1 Gb/s, RTT between endpoints 20 ms (measured, stable)
TCP receive window advertised: 64 KiB (default buffer; confirmed on both ends)
Measured goodput:  26.2 Mb/s (matches the window-bound model)
Link utilization:  ~2.6%
Proposal A (vendor): upgrade the link to 10 Gb/s
Proposal B (vendor): a WAN accelerator ("protocol spoofing")
Proposal C (platform): enlarge TCP socket buffers to 1 MiB window
Backup size:       100 GB = 8 × 10^11 bits
```

### Problem statement
Show why 26.2 Mb/s is the *expected* goodput given the evidence, compute the backup
duration today and under each proposal, and recommend one, with reasoning.

### Evidence pack
The labeled synthetic measurements. Assumptions you may need (state them): RTT and path
stable during the backup; no other traffic; receiver window is the binding limit.

### Constraints
- Use the window–RTT model: throughput ≤ window ÷ RTT.
- Treat 1 Gb/s and 10 Gb/s as link caps in the model.
- One recommendation, justified numerically.

### Student questions
1. Compute the window-bound throughput ceiling for a 64 KiB window and 20 ms RTT.
2. Backup duration at that ceiling for 100 GB.
3. Duration under Proposal A (link 10×), under Proposal C (window 1 MiB), and under
   Proposal B (you argue what it must do to help, given the model).
4. Which proposal do you recommend and why? In one sentence: why is the *vendor's*
   instinct (A) wrong here?

### Expected learning outcomes
- Apply throughput ≤ window/RTT and recognize when links are *not* the bottleneck.
- Compute transfer times from model ceilings.
- Evaluate mitigations against the identified bottleneck (not against vibes).

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Units: 64 KiB is bytes. Convert before dividing by RTT."
2. "Utilization is 2.6% — the fiber is idle. What does that alone tell you about A?"

### Solution
1. 65,536 B × 8 = 524,288 bits; ÷ 0.020 s = **26.2 Mb/s** (matches measurement — the
   model is confirmed, a rare luxury).
2. 8×10^11 ÷ 26.2144×10^6 = **30,517 s ≈ 8 h 29 m** — misses a 6:00 deadline if started
   after ~21:30.
3. **A (10 Gb/s):** link was never the limit → still ≈ 8 h 29 m. **C (1 MiB window):**
   1,048,576 B × 8 ÷ 0.02 = 419.4 Mb/s; time = 8×10^11 ÷ 4.194×10^8 ≈ **1,907 s ≈ 32 min**
   — well within window. **B:** a spoofing accelerator helps by (in effect) using a
   larger effective window / ACK handling on the private segment; it can help, but C
   achieves it with a config change — B's cost/benefit is poor unless RTT or loss is the
   obstacle (here it isn't).
4. Recommend **C**. The vendor's instinct (A) is wrong because the evidence shows a
   window-bound sender on an idle link — utilization 2.6% *refutes* "need more
   bandwidth" before any purchase.

### Reasoning process
Facts: window, RTT, goodput ≈ model ceiling, idle link. Model: throughput ≤ W/RTT, capped
by link. Predict each proposal via the same model. Choose the one that acts on the
binding constraint. Assumptions stated (stability, exclusivity).

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| Recommending A "because Gb/s > Mb/s" | Ignores that the bottleneck is the window, not the link |
| Dividing 100 GB by 1 Gb/s to predict today's time | Assumes link-bound; off by ~40× vs evidence |
| Treating 64 KiB as bits | 512× error; always convert |
| Suggesting parallel connections as free | Multiplies the same per-connection window — valid *technique*, but changes fairness/loss dynamics; accept only with discussion |

### Extension question
At what RTT would a 1 MiB window *stop* being enough for 1 Gb/s? (BDP for 1 Gb/s at RTT
R: window_bits ≥ 10^9 × R → R ≤ 1,048,576×8/10^9 ≈ **8.4 ms**.) What does that predict
for inter-continental transfers, and which knob grows then?
(Expected: buffers must scale with BDP; for RTT 100 ms you need ≥1.25 MB in flight.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Model verified against measurement; all three durations correct; recommendation tied to the binding constraint; B discussed in model terms |
| 3 Proficient | Correct model and C; minor arithmetic slip in durations |
| 2 Developing | Computes ceiling but mispredicts A's effect |
| 1 Beginning | Recommends bandwidth upgrade; no model |

### References
- PD §3.5.2 (flow control; throughput ≤ W/RTT)
- Kurose & Ross §3.5.5 (flow control), §3.7 (TCP congestion control context)
