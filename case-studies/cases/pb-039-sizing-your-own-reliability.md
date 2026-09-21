# PB-039 — Sizing Your Own Reliability (L20, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L20 — Programming the Transport Layer: Reliability over UDP |
| CLOs | CLO5 (window/ARQ arithmetic), CLO4 (protocol design reasoning) |
| In-class slot | Main activity; 25 min, pairs |
| Case type | Design + calculation · Topic: Network programming |
| Evidence policy | Synthetic link parameters, labeled; arithmetic desk-checked (10 Mb/s, 50 ms RTT, 1 KB payloads) |

---

## Student version

### Scenario
The data-science cluster syncs model checkpoints (1 GB each) between two buildings
over a 10 Mb/s cross-link with 50 ms RTT and 1% packet loss. The team's protocol is
reliable-UDP: sequence-numbered 1 KB payloads, cumulative ACKs, retransmit on timeout.
Currently it sends **one packet, waits for its ACK, then sends the next**
(stop-and-wait).

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Link:      10 Mb/s, RTT 50 ms, per-packet loss 1% (independent, teaching model)
Payload:   1,000 B data + 40 B headers = 1,040 B on the wire per packet
Current:   stop-and-wait, retransmit timer 250 ms (fixed)
Target:    1 GB sync must finish in ≤ 15 min
```

### Problem statement
Compute the stop-and-wait ceiling and the window size needed to saturate the link,
compare Go-Back-N vs Selective Repeat at that window under the loss model, and
recommend a design that meets the 15-minute budget.

### Evidence pack
The labeled synthetic parameters. Assumptions to state: independent losses (teaching
model), ACKs never lost, no congestion collapse (dedicated link).

### Constraints
- Show the stop-and-wait utilization formula and each substitution.
- Window math: BDP in packets, then utilization with loss.
- Choose GBN or SR and justify against receiver buffering (the cluster host has
  plenty of RAM — use that fact).

### Student questions
1. Stop-and-wait utilization: show U = (Tx time)/(Tx + 2×prop) style arithmetic with
   the loss factor. What throughput results?
2. How many packets does the 1 GB sync take? How long at the stop-and-wait ceiling —
   does it meet the budget?
3. Window for full rate: compute BDP in bits → packets. With W = BDP and 1% loss
   (each packet retransmitted ~1.01× on average), what's the effective goodput?
4. GBN vs SR at this window: one sentence each on retransmission cost under 1% loss,
   and the recommendation given the RAM fact.

### Expected learning outcomes
- Compute stop-and-wait vs sliding-window utilization with the same loss model.
- Size a window from bandwidth-delay product.
- Choose an ARQ variant from quantified retransmission costs.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Stop-and-wait pays the full RTT for every kilobyte. Write the per-packet cycle
   time first."
2. "Saturating the link means keeping BDP bytes in flight. Convert bits → packets of
   1,000 B."

### Solution
1. Tx = 1,040×8 ÷ 10^7 b/s = 0.832 ms. Cycle (no loss) = Tx + RTT = 50.832 ms.
   With 1% loss: expected cycles per packet ≈ 1/0.99 ≈ 1.0101. Utilization = Tx ÷
   (cycle × 1.0101) ≈ 0.832 ÷ 51.34 ≈ **1.62%**. Throughput = 1,000 B ÷ 50.8 ms
   (per delivered packet) ≈ 1,000×8 ÷ 0.05083 ≈ **157 kb/s** (loss-adjusted ≈ 156 kb/s).
2. 1 GB = 10^9 B → 10^6 packets. At ~156 kb/s: 10^9×8 ÷ 1.56×10^5 ≈ **51,300 s ≈
   14.2 h** — misses the 15-min budget by ~57×.
3. BDP = 10^7 b/s × 0.05 s = 5×10^5 bits = 62,500 B = **62.5 → 63 packets** (round up;
   W = 64 keeps a small margin). Goodput with W = 64: link-rate limited: 10 Mb/s ×
   0.99 ≈ **9.9 Mb/s** ≈ 1,240 kB/s. Sync time = 8×10^9 bits ÷ 9.9×10^6 ≈ **808 s ≈
   13.5 min** ✓ meets budget (with ~10% headroom).
4. GBN: one loss discards up to W−1 packets in flight → at 1% loss per packet with
   W=64, ~48% of windows contain ≥1 loss (1−0.99^64 ≈ 0.475) and each discards on
   average ~32 packets → massive retransmit amplification (expected retransmits per
   delivered packet ≈ 0.475×32 ≈ 15 — wildly over budget). SR: only the lost packet
   retransmits (~1.01×) — costs receiver per-packet buffering (RAM fact ⇒ fine) and
   per-packet ACKs/timers. **Recommend SR with W=64.** (Middle option: GBN with small
   W trades throughput for simplicity — but the numbers above disqualify GBN at W=64;
   show the tension.)

### Reasoning process
Facts: rate, RTT, loss, payload, budget. Model: per-packet cycle → stop-and-wait
ceiling; BDP → window; ARQ variant → retransmission cost. Assumptions: independent
losses, no ACK loss, dedicated link — all stated. Decision by arithmetic.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| U = Tx/RTT (forgets Tx in denominator or the 2×) | Half the cycle is data, half is wait; get the cycle right first |
| W = 63 packets, then compute GBN "fine" | The GBN retransmit amplification at W=64 is the actual killer — window math alone hides it |
| "Just increase the timer" | Timer ≠ window; the ceiling is in-flight bytes, not timeout speed |
| Counting 1 GB as 2^30 B here | Fine if stated — but then 1.074×10^9 B → keep consistency; show which you used |

### Extension question
The cross-link is later shared with an interactive SSH flow. What does your W=64,
no-congestion-control sender do to SSH latency, and what's the minimal fairness fix
within your own protocol? (It fills the pipe with no signal response ⇒ SSH queues
behind 64 KB — latency spikes ~50 ms+ constantly. Minimal fix: respond to loss with
multiplicative decrease (window halves per loss event) and slow-start probing — i.e.,
re-invent AIMD; the exercise's punchline: you've rebuilt TCP's soul.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Cycle arithmetic exact; BDP window; GBN amplification quantified; SR recommendation tied to the RAM fact; budget met with headroom |
| 3 Proficient | Correct window + SR; amplification hand-waved |
| 2 Developing | Computes BDP but misses the ARQ-variant trade-off |
| 1 Beginning | "Use a bigger window" |

### References
- PD §3.4–3.5 (reliable transfer: stop-and-wait, pipelining, GBN, SR) ⚠ verify sections
- Kurose & Ross §3.4 (principles of reliable data transfer)
