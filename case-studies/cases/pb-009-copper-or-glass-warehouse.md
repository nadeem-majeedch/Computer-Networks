# PB-009 — Copper or Glass for the Warehouse? (L05, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L05 — Physical Layer: Signals, Media & Transmission Basics |
| CLOs | CLO1, CLO6 (media trade-offs against physics) |
| In-class slot | Closing consolidation; 12 min, pairs |
| Case type | Trade-off/design · Topic: Network fundamentals (media) |
| Evidence policy | Synthetic requirements, labeled; media limits per standards family, flagged for instructor verification |

---

## Student version

### Scenario
Meridian's warehouse gets 12 new wireless APs and 6 IP cameras. Each AP/camera location is up
to **90 m of horizontal cabling** from the floor cabinet. Three runs pass within 30 cm of
VFD motor drives (an electrically noisy environment). The manager asks: "Just run the
cheap cable everywhere."

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Requirement:   1 Gb/s now; 10 Gb/s "someday" to APs
Runs:          ≤90 m horizontal, star topology to cabinet
Environment:   3 runs near VFD motor drives (EMI)
Budget note:   Cat6 copper ≈ 3–5× cheaper per run than fiber (typical, order-of-magnitude)
```

### Problem statement
Recommend a media plan per run type (normal runs, motor-adjacent runs, AP runs), with
physics-based justification and an explicit statement of what each choice costs.

### Evidence pack
The labeled synthetic requirements. Media properties (attenuation with distance, EMI
immunity, bandwidth-distance limits) come from the lecture; exact category/rating
boundaries are standards-sensitive and marked ⚠ for instructor verification.

### Constraints
- One plan, three run classes; justify each against a physical limit, not a preference.
- State clearly which claims are physics (defensible) vs vendor/standard details
  (verification needed).

### Student questions
1. Which physical phenomena limit copper runs (name at least two) and which limit fiber?
2. For the 90 m runs at 1 Gb/s today: is copper viable? What changes "someday" at 10 Gb/s?
3. For the three motor-adjacent runs: what does EMI do to a copper signal, and what is
   fiber's advantage here?
4. Produce the plan: run class → media → one-line reason → one-line cost.

### Expected learning outcomes
- Tie media choice to physical limits (attenuation, EMI, bandwidth–distance product).
- Distinguish "works today" from "survives tomorrow's requirement".
- Separate defensible physics from standards-detail uncertainty.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Copper's enemies: distance (attenuation), noise (EMI), bandwidth (crosstalk at high
   frequency). Which enemy attacks each run class?"
2. "The AP runs are the ones with a 'someday' requirement. Solve for someday, not today."

### Solution
1. Copper: attenuation (signal weakens with length), EMI/crosstalk (noise coupled onto
   the pair; worse at higher frequencies), bandwidth limits (channel rating at
   distance). Fiber: attenuation is far lower per distance; immune to EMI (glass
   carries light, not charge); bandwidth limited by optics, not the medium over these
   distances.
2. 1 Gb/s at ≤90 m on Cat6-class copper: viable (100 m channel is the classic horizontal
   limit ⚠ verify category specifics). At 10 Gb/s: marginal-to-infeasible on older
   categories at that length; plan optics or certified 10G-capable copper ⚠.
3. EMI induces noise on copper → errors → retransmissions; fiber is immune to
   electromagnetic coupling. For motor-adjacent runs, fiber (or shielded, properly
   bonded copper as a budget fallback ⚠) is the defensible call.
4. Plan: normal 90 m runs → copper (cheap, meets 1 G; upgrade path documented); motor-
   adjacent runs → fiber (physics: EMI immunity); AP runs → fiber or certified-10G
   copper (solves "someday" without recabling). Cost: fiber front-loaded, avoids rework.

### Reasoning process
Facts: distances, EMI sources, current + future bandwidth. Model: each media's failure
mode vs each constraint. Classify runs → match media to dominant failure mode → total
cost of ownership (rework beats cable-price delta).

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Cheap cable everywhere" | Ignores EMI runs (physics) and the 10 G future (rework cost) |
| "Fiber everywhere" | Pays a premium where copper physics is fine; not wrong, but unexamined |
| Treating 100 m as exact for all categories | Category- and speed-dependent ⚠; must be flagged |
| Ignoring the AP "someday" | Locks in recabling at the worst time (ceiling work) |

### Extension question
One motor-adjacent run is 140 m — beyond even fiber-friendly horizontal assumptions for
copper. What changes? (Copper is now out on length alone ⚠; fiber's attenuation
advantage makes it the only practical choice — distance flips from "EMI factor" to
"deciding factor".)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Per-class plan with named physical mechanisms; future-proofing explicit; verification flags present |
| 3 Proficient | Correct media choices; one mechanism misattributed |
| 2 Developing | Chooses by cost alone; no physics |
| 1 Beginning | "Fiber is better" with no criterion |

### References
- PD §2.3 (physical media: twisted pair, fiber, properties)
- Tanenbaum & Wetherall Ch. 2 (media characteristics) ⚠ verify edition/section
