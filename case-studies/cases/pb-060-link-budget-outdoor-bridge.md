# PB-060 — Will the Rooftop Bridge Survive the Rain? (L30, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L30 — Mobile & Wireless Enterprise Networking |
| CLOs | CLO5 (link-budget arithmetic), CLO6 (margin verdicts) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Calculation · Topic: Wireless networking (link budget) |
| Evidence policy | Synthetic radio specs, labeled; FSPL constant 32.44 (f in MHz, d in km) — arithmetic desk-checked |

---

## Student version

### Scenario
Meridian wants a point-to-point Wi-Fi bridge between HQ-A's roof and a warehouse 3 km
away (fiber trenching is too expensive). The vendor quotes gear; you must check the
physics *before* the purchase order.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Frequency:        5.8 GHz (5800 MHz)
Distance:         3 km
TX power:         +24 dBm (both ends)
Antenna gains:    +23 dBi dish, each end
Cable/connector loss: 2 dB per end
RX sensitivity (at required MCS): −74 dBm
Weather margin target: ≥ 15 dB (rain/fade allowance)
FSPL(dB) = 32.44 + 20·log10(f_MHz) + 20·log10(d_km)
```

### Problem statement
Compute FSPL, the received signal strength (RSL), the fade margin, and deliver a
go/no-go verdict against the 15 dB target — showing every dB.

### Evidence pack
The labeled synthetic radio specs. The FSPL formula is given; everything else is
bookkeeping. Assumptions to state: free-space propagation (no Fresnel obstruction —
verified by the site survey), no interference.

### Constraints
- Every term signed correctly (gains +, losses −).
- Verdict must reference the target margin explicitly.

### Student questions
1. FSPL for 5800 MHz at 3 km (show the log arithmetic; approximate log values
   given: log10(5800) ≈ 3.763, log10(3) ≈ 0.477).
2. RSL at the warehouse receiver: TX + gains − losses − FSPL. Show each term.
3. Fade margin = RSL − sensitivity. Verdict vs the 15 dB target?
4. Sensitivity check: if the link instead required the *higher* MCS (−66 dBm
   sensitivity), what's the margin now — and which MCS would you order?

### Expected learning outcomes
- Compute free-space path loss and full link budgets with signed terms.
- Deliver margin-based go/no-go verdicts.
- Connect MCS selection to sensitivity and margin.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "FSPL = 32.44 + 20·log(f) + 20·log(d). Compute each log term before adding."
2. "RSL = TX + antenna gains − cable losses − FSPL. Then margin = RSL − sensitivity.
   The verdict falls out of the last subtraction."

### Solution
1. FSPL = 32.44 + 20×3.763 + 20×0.477 = 32.44 + 75.26 + 9.54 ≈ **117.2 dB**.
   (Desk-check: 5.8 GHz at 3 km sits between the familiar 100 dB@1 km and 106
   dB@2 km figures for 2.4 GHz — plausibility ✓.)
2. RSL = +24 + 23 + 23 − 2 − 2 − 117.2 = **−51.2 dBm**.
3. Margin = −51.2 − (−74) = **22.8 dB** ≥ 15 dB ⇒ **GO** — with headroom for rain
   fade and alignment drift.
4. At −66 dBm sensitivity: margin = −51.2 − (−66) = **14.8 dB** < 15 ⇒ marginal —
   technically close but below target. Order the lower MCS (the −74 dBm radio
   config): the 3 km link's throughput at that MCS still dwarfs the trenching
   alternative, and the margin buys reliability. (Teaching point: "faster MCS" is
   not free — it spends your fade margin.)

### Reasoning process
Facts: radio specs, distance, frequency, target margin. Model: link budget = signed
sum; verdict = margin vs target. The MCS question shows sensitivity is a *choice*
with margin consequences — the budget drives the order, not the datasheet.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| Adding cable loss as +2 dB | Losses subtract; sign errors flip the verdict near marginal cases |
| Using 32.44 with f in GHz and d in km | The constant assumes MHz; unit discipline is the whole exercise |
| "22.8 dB margin, so use the faster MCS too" | MCS choice consumes margin; the 15 dB target is per-*configuration* |
| Ignoring Fresnel clearance | Free-space assumes clear first Fresnel zone (site-survey fact, stated); a roof-edge obstruction breaks the model entirely |

### Extension question
Rain fade at 5.8 GHz is modest, but the same link at 24 GHz would suffer heavily.
Using the same budget structure, what changes *besides* FSPL (which rises ~12 dB) if
the wavelength shrinks ~4×? (FSPL +~12.3 dB (20log₁₀(24000/5800)); antenna gain for
same dish size rises ~12 dB (aperture physics) — partly self-compensating; but
rain attenuation at 24 GHz becomes a real per-km dB term requiring its own margin
line ⚠ ITU-R models — the budget structure absorbs new terms; that's the point of
the method.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | FSPL with log steps; signed budget; margin verdicts for both MCS options; Fresnel/unit assumptions stated |
| 3 Proficient | Arithmetic right; one sign or unit slip |
| 2 Developing | FSPL only; no budget or verdict |
| 1 Beginning | "The vendor says it works" |

### References
- PD §2.3/§7 (wireless link fundamentals) ⚠ verify section mapping
- FSPL 32.44 constant: standard engineering formula (f in MHz, d in km) ⚠ verify
  against course text; ITU-R P.530 for rain-fade modeling ⚠
