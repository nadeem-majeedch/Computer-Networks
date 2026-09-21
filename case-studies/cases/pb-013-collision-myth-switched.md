# PB-013 — "Collisions Are Slowing Me Down" (L07, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L07 — MAC Protocols & Wired LANs: Ethernet |
| CLOs | CLO2 (explain CSMA/CD scope), CLO6 (evaluate a claim against evidence) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Conceptual claim-check · Topic: Ethernet |
| Evidence policy | Synthetic claim + evidence, labeled; internally consistent |

---

## Student version

### Scenario
A teammate posts in the group chat: "Our transfers are slow because of Ethernet
collisions — that's what CSMA/CD is for, and old books say it kills performance." The
transfers run between two Meridian PCs connected to the **same switch**, both NICs
report 1 Gb/s **full-duplex**.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Both NICs:        1000BASE-T, full-duplex, link up
Connection:       each PC has its own switch port (no hubs anywhere)
Switch counters:  0 collisions (counter category not even supported on this switch)
Measured:         iperf3 ~940 Mb/s between the two PCs
Claim:            "collisions are killing our throughput"
```

### Problem statement
Evaluate the claim. Explain what CSMA/CD is for, why it cannot be the cause here, and
what mechanism actually governs throughput on this link.

### Evidence pack
The labeled synthetic evidence. One flagged nuance: on full-duplex switched Ethernet,
collision-based media access does not exist on the link.

### Constraints
- Use the evidence; do not argue from history alone.
- State what *would* have to be true for the claim to make sense (and why it isn't).

### Student questions
1. What problem did CSMA/CD solve, and on what kind of shared medium?
2. Why is a collision physically impossible on this link? (Be precise about pairs and
   direction.)
3. What governs throughput here instead — name the mechanism that limits a single TCP
   flow below 1 Gb/s.
4. Rewrite the teammate's sentence so it is true.

### Expected learning outcomes
- Scope CSMA/CD to half-duplex shared media; exclude it from switched full-duplex.
- Explain why full-duplex removes collisions structurally (separate TX/RX paths).
- Identify the real throughput governor (e.g., TCP window/congestion control, encoder
   overhead).

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Collisions happen when two stations *share* one channel and both talk. Do these two
   PCs share anything?"
2. "940 Mb/s out of 1000 — the missing 6% is overhead, not fights over the wire."

### Solution
1. CSMA/CD arbitrated access on shared half-duplex media (coax buses, hubs): stations
   sensed the carrier, transmitted, detected simultaneous transmission, backed off.
2. With 1000BASE-T full-duplex, each direction has its own pair set; a port receives
   only on RX pairs and transmits only on TX pairs. There is no shared channel and no
   carrier sense at the MAC — collisions cannot occur. The switch's collision counter
   doesn't even exist on this hardware.
3. Throughput is governed by (a) encoding/IFG/preamble overhead (small %), and (b) the
   transport layer: TCP congestion window and flow control decide how much is in flight —
   the measured 940 Mb/s is consistent with overhead + TCP behavior on a healthy 1 Gb/s
   link. (Link is essentially perfect.)
4. True version: "Our transfers reach ~94% of line rate — normal overhead for a healthy
   full-duplex switched link; collisions are not part of this architecture."

### Reasoning process
Facts: full-duplex, per-port switching, zero-collision counters, 940 Mb/s. Model:
collision requires a shared channel; none exists. Reject the claim on mechanism +
measurement; attribute the residual gap to overhead/TCP, which is expected.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| Quoting old textbooks uncritically | CSMA/CD answers existed for *shared* Ethernet; architecture changed |
| "Collisions might still happen inside the switch" | Switch ports are point-to-point; no shared medium inside |
| "940 < 1000 so something is wrong" | ~5–6% overhead is normal; the claim misreads the baseline |

### Extension question
When *would* the teammate's sentence have been true in this building? (If a hub were
installed, or NICs forced to half-duplex on a shared segment — connecting PB-012's
mismatch mechanism: forced-half on one end reintroduces collision territory even on
twisted pair.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Mechanism-level impossibility argument + evidence use; real throughput governor named; rewritten claim accurate |
| 3 Proficient | Correct rejection; mechanism slightly vague on pairs/direction |
| 2 Developing | "Switches prevent collisions" asserted without mechanism |
| 1 Beginning | Accepts the claim; no evidence use |

### References
- PD §6.3.2 (CSMA/CD and its obsolescence in switched Ethernet)
- Kurose & Ross §6.3.2; Spurgeon, *Ethernet: The Definitive Guide* (duplex modes) ⚠ verify edition
