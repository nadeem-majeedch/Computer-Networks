# PB-002 — How Long Is a Packet's Cross-Campus Trip? (L01, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L01 — What Is a Network? |
| CLOs | CLO1, CLO5 (quantitative reasoning about networks) |
| In-class slot | Closing consolidation; 12 min, pairs |
| Case type | Calculation · Topic: Network fundamentals |
| Evidence policy | Synthetic evidence, labeled; arithmetic shown in solution is internally consistent |

---

## Student version

### Scenario
Two analytics servers sit in HQ-A and HQ-B, connected by a **2 km fiber link** running at
**1 Gb/s**. The data-science team asks: "If I send one ping between buildings, how fast
*could* it possibly come back?" You answer with a floor, not a guess.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Link:      2 km fiber, 1 Gb/s Ethernet
Physics:   signal speed in fiber ≈ 2 × 10^8 m/s
Frame:     1500-byte frame for the ping payload
Question:  round-trip time (RTT) floor for one 1500-byte frame each way
```

### Problem statement
Compute the **minimum possible RTT** for a 1500-byte frame traveling HQ-A → HQ-B → HQ-A,
showing each delay component, and state clearly what real pings add beyond your floor.

### Evidence pack
The labeled synthetic facts above. Any additional time (processing, queuing) is an
**assumption** you must state, not a fact.

### Constraints
- Show every step and unit; no answer without arithmetic.
- Model serialization simply (one frame fully transmitted per direction).
- Do not use a "speed of light in vacuum" — fiber is slower.

### Student questions
1. Propagation delay, one way, in µs.
2. Serialization (transmission) delay for one 1500-byte frame at 1 Gb/s, in µs.
3. RTT floor: request frame + reply frame, propagation + serialization. Give µs and ms.
4. A real `ping` between these buildings shows ~0.2 ms. In one sentence each: name two
   delay components your floor excludes, and explain why the floor is still the right
   thing to compute first.

### Expected learning outcomes
- Separate propagation delay from serialization delay and compute both.
- Understand RTT as a *sum* of components and compute a physical floor.
- Distinguish measured values from computed bounds (facts vs. assumptions).

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Distance ÷ speed gives time. Which distance — one way or round trip?"
2. "Bits on the wire: frame size ÷ link rate. Watch bits vs. bytes."

### Solution
1. Propagation one way: 2000 m ÷ (2×10^8 m/s) = **10 µs**.
2. Serialization: 1500 B = 12,000 bits; 12,000 ÷ 10^9 b/s = **12 µs**.
3. RTT floor = 2×(10 µs propagation) + 2×(12 µs serialization) = 20 + 24 = **44 µs ≈ 0.044 ms**.
4. Excluded: switch/router processing and queuing delays, and any Wi-Fi or access-link
   time if hosts aren't directly on the fiber. The floor is right first because it is
   *physics you cannot beat* — every real RTT ≥ floor, so a measured 0.2 ms tells you
   ~0.156 ms is soft (processing/queuing), which is where optimization would look.

### Reasoning process
Facts: distance, rate, signal speed, frame size. Model: RTT = 2×(prop + serialization).
Compute components → sum → compare with measurement → attribute the difference to stated
assumptions (processing, queuing).

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| Using 3×10^8 m/s | That's vacuum; fiber ≈ 2×10^8 m/s |
| Counting serialization once for the round trip | The reply frame is also serialized |
| Mixing bytes and bits in one division | 1500 B must become 12,000 bits before dividing by b/s |
| Reporting only propagation | Serialization dominates at 1 Gb/s here (12 µs vs 10 µs) |

### Extension question
If the link ran at 100 Mb/s instead, which delay component doubles, and what is the new
RTT floor? (Serialization: 120 µs each way → floor 2×(10+120) = 260 µs ≈ 0.26 ms.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | All three computations correct with units; Q4 distinguishes fact (floor) from assumption (processing) |
| 3 Proficient | One arithmetic slip; reasoning otherwise complete |
| 2 Developing | Computes propagation but conflates serialization; floor overstated |
| 1 Beginning | Guesses an RTT; no component model |

### References
- PD §1.4 (delay components: nodal processing, queuing, transmission, propagation)
- Kurose & Ross §1.4.2 (delay, loss, throughput)
