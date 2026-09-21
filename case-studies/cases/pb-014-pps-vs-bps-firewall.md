# PB-014 — Packet Rate, Not Bandwidth, Kills the Box (L07, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L07 — MAC Protocols & Wired LANs: Ethernet |
| CLOs | CLO5 (rate calculations), CLO6 (capacity evaluation) |
| In-class slot | Main activity; 15 min, pairs |
| Case type | Calculation · Topic: Ethernet/performance |
| Evidence policy | Synthetic spec numbers, labeled; arithmetic desk-checked (1.49 Mpps at 64 B) |

---

## Student version

### Scenario
Meridian buys a "1 Gb/s firewall" for the analytics VLAN boundary. Marketing quotes
bandwidth. The vendor's fine print lists "throughput: 1 Gb/s (IMIX); 0.35 Mpps for
64-byte frames". During a DNS-heavy afternoon, the box drops packets at only ~300 Mb/s
of traffic.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Firewall spec:     1 Gb/s quoted; 0.35 Mpps small-packet ceiling
Observed mix:      DNS responses, small ACKs — average frame ≈ 100 B on the wire
Ethernet on-wire overhead per frame: preamble 8 B + IFG 12 B (= 20 B beyond the frame)
Claim to analyze:  "1 Gb/s firewall" vs the 300 Mb/s failure
```

### Problem statement
Compute the wire rate in packets/second for 64 B frames at 1 Gb/s, explain the 0.35 Mpps
spec (what consumes the difference between your wire-rate figure and the box's ceiling),
and show why the firewall fails at 300 Mb/s under this traffic mix.

### Evidence pack
The labeled synthetic spec and observed mix. Assumptions to state: the 0.35 Mpps ceiling
is the box's *processing* limit (per-packet work), not a wire limit.

### Constraints
- Show the pps arithmetic including preamble/IFG.
- Keep "why the box is slower than the wire" at the architecture level (per-packet
  processing cost); no vendor internals.

### Student questions
1. At 1 Gb/s, how many 64 B frames/s can the *wire* carry (count preamble + IFG)?
2. The spec says the box caps at 0.35 Mpps. Roughly how many times more work does the
   box do per packet than the wire's theoretical minimum? (Just the ratio; speculate
   only in one labeled sentence.)
3. For the observed 100 B average frames: how many pps does 300 Mb/s correspond to? Is
   that within the box's ceiling? Then explain the failure anyway.
4. The vendor says "upgrade to the 10 Gb/s model." What single spec number should
   Meridian check *instead*, and what value would it need for this mix?

### Expected learning outcomes
- Compute line-rate pps including Ethernet framing overhead.
- Distinguish bandwidth (bps) capacity from per-packet processing capacity (pps).
- Match a traffic *mix*, not a headline number, to a device's spec.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "The wire carries more than the frame: 64 B payload + 20 B of framing every time."
2. "Divide total bits/s by bits per frame — including the overhead bytes."

### Solution
1. On-wire per frame = (64 + 20) B = 84 B = 672 bits. Wire rate = 10^9 / 672 ≈
   **1.49 Mpps** (1,488,095 pps).
2. 1.49/0.35 ≈ **4.3×** — the box spends ~4× the per-packet time budget vs pure wire
   movement (Labeled speculation: policy lookups, NAT/state tables, inspection consume
   cycles per packet).
3. 100 B frames = (100+20)×8 = 960 bits. 300 Mb/s = 3×10^8 / 960 ≈ **312,500 pps ≈
   0.312 Mpps** — within 0.35 Mpps, so pps alone doesn't explain it; the failure needs
   the *concurrent* load factor: the 0.35 Mpps ceiling is for small frames alone, but
   the box also carries other flows + sessions; under mixed load the effective per-
   packet budget shrinks (or the spec's ceiling assumed no features enabled). The
   teaching point: a single spec number is not a capacity model — mix and feature set
   both bite. (State clearly: this last step is reasoning about spec ambiguity, flagged
   for instructor verification against a real datasheet.)
4. Check the **small-packet pps** spec (e.g., "64-byte frame rate"). Need: worst-case
   mix at ~64 B: 1 Gb/s needs 1.49 Mpps; the current box offers 0.35 — so the needed
   spec is ≥1.5 Mpps *regardless of the Gb/s marketing number*.

### Reasoning process
Facts: spec pps ceiling, observed mix/average frame size, failure at 300 Mb/s. Model:
wire pps = rate ÷ bits-per-frame; box capacity = pps ceiling; compare mix-derived pps to
ceiling, then reconcile the residual via spec ambiguity (labeled). Action: match the
*pps* spec to the mix.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| 10^9/(64×8) ≈ 1.95 Mpps | Ignores the 20 B/frame wire overhead (preamble+IFG) |
| Buying by bps alone | Small-packet workloads are per-packet-bound; the current outage proves it |
| "300 Mb/s < 1 Gb/s so it can't be the firewall" | bps and pps are different resources; the mix converts bandwidth into packets |
| Assuming spec pps holds with all features on | Datasheet ceilings usually assume minimal config ⚠ verify per vendor |

### Extension question
A defense team proposes jumbo frames (MTU 9000) on the segment to "fix" the firewall.
Compute the new wire pps at 1 Gb/s for 9000 B frames ((9000+20)×8 = 72,160 bits →
13,858 pps) and explain when this is and isn't a legitimate fix. (Legitimate for bulk
flows you control; useless for DNS/small-ACK traffic, which stays small — and mixed-MTU
segments add PMTUD hazards to flag.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | 1.49 Mpps correct with overhead; mix conversion correct; spec-ambiguity reasoning labeled; identifies pps as the spec to check |
| 3 Proficient | Arithmetic right; misses the within-ceiling subtlety in Q3 |
| 2 Developing | Computes pps without wire overhead |
| 1 Beginning | Accepts the bps spec at face value |

### References
- PD §6.3 (Ethernet frame format/preamble/IFG), §1.4 (transmission delay per packet)
- Spurgeon, *Ethernet: The Definitive Guide* (line-rate pps tables) ⚠ verify edition
