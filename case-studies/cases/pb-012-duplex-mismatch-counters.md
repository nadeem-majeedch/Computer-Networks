# PB-012 — The Port That Lies in Daylight (L06, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L06 — Data Link Layer: Framing, Errors & Reliability |
| CLOs | CLO2, CLO6 (diagnose L1/L2 faults from counters) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Diagnostic · Topic: Ethernet/physical faults |
| Evidence policy | Synthetic counter dumps, labeled; counter semantics real, values illustrative |

---

## Student version

### Scenario
Every afternoon, the analytics PC on floor 3 feels "laggy"; mornings are fine. The
morning-shift tech finds nothing. You pull the switch-port counters.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Port 3/12 (to the analytics PC), 24 h counters:
  FCS errors:        18,204
  Late collisions:   6,310
  Runts:             3,912
  CRC (received):    concentrated 14:00–18:00, near-zero overnight
  Speed/duplex:      100 Mb/s, HALF-duplex  (PC NIC also shows 100/Half)
Link never goes down. ping is clean at all hours when idle.
```

### Problem statement
Diagnose the fault from the counter pattern, explain each counter's meaning at the frame
level, and explain the afternoon-only timing without inventing facts.

### Evidence pack
The labeled synthetic counter dump. Known facts: both ends report 100/Half; the link
never drops. Unknown: why the NIC negotiated half — you may hypothesize but must label
it.

### Constraints
- Explain what a late collision *is* (frame-level) and why half-duplex produces them.
- Distinguish "evidence supports" from "plausible but unproven".
- Fix must come with a verification step.

### Student questions
1. Decode each counter: FCS error, late collision, runt — what does each say happened to
   frames on this port?
2. Why does half-duplex cause exactly this signature?
3. Why only afternoons? Give a hypothesis consistent with the timing and label it as
   hypothesis.
4. State the fix and the verification that proves it.

### Expected learning outcomes
- Read Ethernet port counters as frame-level evidence.
- Explain duplex mismatch mechanics (carrier sense fails → collisions late in frames).
- Separate measured fact from plausible-but-unproven cause.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "In half-duplex, a station transmits while *listening*. What happens if the other
   station starts transmitting mid-frame — and who notices first?"
2. "Both ends *claim* 100/Half. Autonegotiation had to fail somewhere — that's a
   hypothesis, not a fact. What would you check?"

### Solution
1. FCS errors: frames arriving with bad checksums — corrupted in transit (collisions or
   noise). Late collisions: a collision detected *after* the 64-byte collision window —
   only possible when another station transmits mid-frame, i.e., two senders on a
   segment that shouldn't have two senders (half-duplex). Runts: frames shorter than
   64 B, the debris of collisions.
2. In half-duplex, both ends use CSMA/CD: they may sense the medium idle and transmit
   concurrently. The PC transmits long frames while the switch (or vice versa) starts
   sending → collision late in the frame → garbage both ways → FCS errors, runts, late
   collisions. In full-duplex this is impossible (each direction has its own pair/path).
3. Hypothesis (label it): afternoon load makes both stations transmit simultaneously
   often — collisions need *concurrency*, and idle mornings produce almost none. The
   mismatch exists all day; the damage is load-dependent.
4. Fix: configure both ends explicitly to 100/Full (or restore working autonegotiation).
   Verify: counters reset → 24 h later FCS errors ≈ 0, late collisions = 0, sustained
   throughput test (e.g., 60 s copy) clean. If NIC won't do full at that speed ⚠, check
   cable (some 100-MbS full-duplex need all 4 pairs) before concluding.

### Reasoning process
Facts: 100/Half both ends; late collisions + FCS + runts clustered with load. Model:
half-duplex ⇒ collisions possible ⇒ late collisions corrupt frames; load correlates
with symptom timing. Hypothesis: negotiation failure (autoneg off on one side or
mismatched config) — unproven until checked, but the *mechanism* is established by the
counter signature alone.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Bad cable" alone | Explains FCS errors, not late collisions — collisions require a second transmitter |
| "Replace the switch port" | Same signature would return; the duplex policy is the cause |
| "It's the afternoon, so it's the air conditioning" | Correlation hunt without mechanism; counters already explain timing via load |
| Set both to half | Hides the symptom partially; throughput stays terrible; collisions remain |

### Extension question
A vendor proposes "collision-domain analyzer" software for the PC. Given the evidence,
what single config check would give the same answer for free? (Read the NIC's actual
negotiated settings vs its configured ones; if configured "auto" but link partner is
forced, the classic mismatch appears — one `ethtool`/adapter-properties look.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | All three counters decoded at frame level; mechanism complete; hypothesis clearly labeled; verification step present |
| 3 Proficient | Correct diagnosis; counters partially decoded |
| 2 Developing | "Bad cable/switch" conclusions; ignores half-duplex mechanism |
| 1 Beginning | Reboots hardware; no counter analysis |

### References
- PD §6.3 (Ethernet: CSMA/CD history, frame format, collisions)
- Kurose & Ross §6.3.2 (Ethernet CSMA/CD); IEEE 802.3 autonegotiation behavior ⚠ verify
