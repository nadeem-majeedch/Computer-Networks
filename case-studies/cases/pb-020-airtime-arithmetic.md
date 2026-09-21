# PB-020 — One Channel, Three Hungry Clients (L10, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L10 — Wireless Networking: Wi-Fi Fundamentals |
| CLOs | CLO5 (shared-medium arithmetic), CLO6 (evaluate capacity claims) |
| In-class slot | Main activity; 15 min, pairs |
| Case type | Calculation · Topic: Wireless networking / performance |
| Evidence policy | Synthetic measurements, labeled; rounding rules stated; illustrative values flagged |

---

## Student version

### Scenario
A single AP serves the analytics corner. Three jobs run at once: a 2 GB dataset pull,
a video call, and periodic telemetry. The team lead claims "the AP is 600 Mb/s, so the
dataset pull will take 27 seconds." It takes much longer.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (values illustrative):**

```
Link rates negotiated:
  Laptop (dataset pull):  433 Mb/s PHY
  Phone (video call):     87 Mb/s PHY
  Sensor gateway:         54 Mb/s PHY
Channel: one 80 MHz 5 GHz channel, no external contention (measured)
Efficiency factor (MAC overhead, ACKs, aggregation): ≈55% of PHY rate as
  effective single-client throughput when a client has the air to itself
  (illustrative; real value varies with frame sizes and retries)
Call + telemetry requirements: call needs ≈2 Mb/s steady; telemetry ≈1 Mb/s
Dataset: 2 GB = 2 × 10^9 bytes
```

### Problem statement
Build an airtime budget: how much channel capacity remains for the dataset pull while
the call and telemetry run, and how long does the pull really take? Compare with the
team lead's claim.

### Evidence pack
The labeled synthetic rates. Assumptions to state: efficiency factor applies
uniformly; no retries surge; airtime is divided between *transmitting* clients, not
between their PHY rates.

### Constraints
- Work in *airtime fractions*, not PHY-rate leftovers.
- State the rounding rule you use at the end.

### Student questions
1. Effective single-client throughput at each negotiated rate (apply the 55% factor).
2. What *airtime fraction* do the call and telemetry need together?
3. Remaining airtime for the dataset pull, and the resulting throughput for the pull.
4. Pull duration vs the lead's 27 s claim. What two oversimplifications does the claim
   make?

### Expected learning outcomes
- Reason about shared-medium capacity in airtime rather than rate sums.
- Compute effective throughput under fractional airtime allocation.
- Identify the mistakes in a "divide the headline rate" claim.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "The medium is the resource, not the megabits. Convert each stream's *need* into a
   share of the clock."
2. "If the call needs 2 Mb/s of a 238 Mb/s-effective stream, it needs almost no time at
   all. The heavy consumer is the one that transfers continuously."

### Solution
1. Single-client effective: laptop 433×0.55 ≈ 238 Mb/s; phone 87×0.55 ≈ 48 Mb/s;
   gateway 54×0.55 ≈ 30 Mb/s.
2. Call: 2/48 ≈ 4.2% airtime. Telemetry: 1/30 ≈ 3.3%. Together ≈ **7.5%** (they don't
   block each other materially at these needs).
3. Remaining airtime ≈ 92.5% → dataset pull throughput ≈ 238 × 0.925 ≈ **220 Mb/s**
   ≈ 27.5 MB/s. (Rounding rule: keep 2–3 significant figures; PHY rates are already
   nominal.)
4. Duration = 2×10^9 B ÷ 27.5 MB/s ≈ **73 s** — roughly 2.7× the claim. The claim's two
   errors: (a) treats the AP's *aggregate marketing rate* as a per-client rate (433 ≠
   600, and 433 is a PHY number needing the efficiency haircut); (b) ignores that the
   shared airtime is consumed by *everyone transmitting*, including the pull's own ACK
   traffic and the other clients. (Also: 600 Mb/s is likely a box-total figure, not
   per-radio-per-client.)

### Reasoning process
Facts: negotiated rates, efficiency factor, stream needs. Model: airtime is the scarce
unit; convert needs → airtime fractions; subtract from 1; scale the pull's effective
rate. Distinguish facts (rates, needs) from assumptions (uniform efficiency, no retry
storms) and flag them.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| 600 − 2 − 1 ≈ 597 Mb/s for the pull | Rates aren't airtime; the pull can't exceed its own negotiated, efficiency-limited rate |
| Dividing 433 equally among 3 clients | Fair-share scheduling is not the model here; *need* sets the split |
| Using PHY rate directly (433 → 54 s) | Ignores MAC efficiency (~55%) and contention with the client's own ACKs |
| Forgetting the call's share entirely | 7.5% is small but nonzero; also the *comparison* to the claim is the point |

### Extension question
A fifth station starts a video stream needing 8 Mb/s from a 30 Mb/s-effective link.
Recompute the pull time and discuss which assumption breaks first as clients multiply.
(8/30 ≈ 26.7% airtime; pull ≈ 238×(1−0.075−0.267) ≈ 157 Mb/s → ≈102 s. First casualty:
the "no retry surge" assumption — aggregate load pushes retransmissions up, and the
efficiency factor sags.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Airtime fractions correct; pull ≈ 220 Mb/s / ≈73 s; names both claim errors; assumptions stated |
| 3 Proficient | Method right; arithmetic or rounding slip |
| 2 Developing | Subtracts rates instead of airtime |
| 1 Beginning | Accepts the 27 s claim |

### References
- PD §7.3 (802.11 MAC: CSMA/CA, ACKs) ⚠ verify section
- Kurose & Ross §7.3.2 (802.11 MAC protocol)
