# PB-058 — The Dashboard That Lied (L29, Advanced)

| Field | Value |
|---|---|
| Difficulty | **Advanced** |
| Lecture(s) | L29 — Monitoring, Telemetry & Systematic Troubleshooting |
| CLOs | CLO5 (counter arithmetic), CLO6 (audit a measurement pipeline) |
| In-class slot | Extended activity; 25 min, groups of 3 |
| Case type | Diagnostic (measurement audit) · Topic: Monitoring/performance |
| Evidence policy | Synthetic counter dumps, labeled; wrap arithmetic desk-checked; MIB-II semantics flagged for verification |

---

## Student version

### Scenario
The new 10 Gb/s analytics uplink "shows 3.1 Gb/s max" on the dashboard, and one port
occasionally reports **negative** throughput. The network team suspects the link;
the data-science team (which pushed 8.5 Gb/s in a controlled test) suspects the
dashboard. You audit the measurement chain.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (illustrative values):**

```
Device:  10 Gb/s port; MIB-II style counters (classic 32-bit octet counters)
         ifSpeed reported: 4294967295  (the 32-bit maximum)
         ifHighSpeed reported: 10000   (Mb/s)
Poller:  polls ifInOctets (32-bit) every 60 s; computes rate = Δoctets/Δt
Observations:
  Busy hour:   rate spikes to ~3.1 Gb/s then "wraps" to negative on one sample
  Quiet hour:  rate readings look plausible (≤1.2 Gb/s)
Test:   controlled 8.5 Gb/s push for 60 s → dashboard shows ~1.1 Gb/s (?!)
32-bit octet counter wrap time at line rate: 2^32 B ÷ (10×10^9/8 B/s) ≈ 3.44 s
Poller notes: single-sample delta; no wrap detection; no counter-discontinuity check
```

### Problem statement
Explain each artifact with counter arithmetic (the 3.1 Gb/s ceiling, the negative
sample, the 8.5 Gb/s test reading 1.1), identify the two missing pipeline features,
and specify the correct 64-bit polling design.

### Evidence pack
The labeled synthetic counter evidence. Facts: 32-bit counters, 60-s polls, wrap
time ≈3.4 s at 10G, ifSpeed capped, ifHighSpeed correct. The three artifacts are
one root cause wearing three hats — plus one bandwidth-cap subtlety.

### Constraints
- Each artifact gets its own arithmetic walk (no hand-waving to "counter wrap").
- The fix must state wrap detection and discontinuity handling explicitly.

### Student questions
1. Why does the dashboard *never* exceed ~3.1 Gb/s on this link? Show the arithmetic
   (what does Δoctets max out at between two 60-s polls... careful — it *wraps*;
   explain the ceiling that survives).
2. One sample shows negative rate: reconstruct the arithmetic that produces a
   negative delta from an unsigned counter.
3. The 8.5 Gb/s test read ~1.1 Gb/s. Reconstruct: at 8.5 Gb/s, how many 32-bit
   wraps occur per 60-s poll, and what does Δ = current − previous become after
   k full wraps? (Modular arithmetic walk.)
4. Fixes: (a) poll which OID, (b) what wrap/discontinuity handling must the poller
   add, (c) what does ifSpeed vs ifHighSpeed teach about the 3.1 ceiling? Wait —
   assign: which artifact does *each* fix address?

### Expected learning outcomes
- Compute 32-bit counter wrap times at given rates.
- Explain delta-based rate computation failure modes (ceiling, negative, modular
  collapse).
- Specify a correct 64-bit counter pipeline with discontinuity handling.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "A 32-bit octet counter at 10 Gb/s laps every ~3.4 seconds. A 60-second poll
   window laps it ~17 times. What does 'difference of two counters' return when the
   odometer lapped 17 times?"
2. "Unsigned counters never go negative — but *differences of them* can, when the
   later sample is numerically smaller."

### Solution
1. The *ceiling* artifact: between polls the counter wraps k times; the observed Δ
   = (C₂ − C₁) mod 2³² — i.e., only the *residue* survives. Maximum believable
   residue ≈ 2³² B = 4.295 GB per 60 s ⇒ 4.295×8/60 ≈ **573 Mb/s**... reconcile
   with the reported 3.1 Gb/s ceiling: honest reconciliation — the 3.1 Gb/s ceiling
   comes from the poller's *clamp* (many pollers reject implausible spikes > port
   speed × fudge and report the previous value, or the vendor's delta-clamp at
   2^32/2) ⚠ implementation-dependent — the arithmetic floor is 573 Mb/s and the
   observed 3.1 Gb/s sits between; the *teaching* resolution: without knowing the
   poller's clamping rule you cannot predict the exact artifact — that uncertainty
   is itself the lesson (the measurement pipeline is unspecified, hence untrusted).
   What *is* provable: at 8.5 Gb/s the counter laps ~17.6× per window; any
   single-delta reading is modular garbage.
2. Negative rate: C₂ < C₁ numerically (wrap landed between them) ⇒ signed
   subtraction yields C₂ − C₁ < 0; the poller's signed interpretation prints a
   negative rate. (Unsigned delta with wrap-aware modulus — `(C₂ − C₁) mod 2³²` —
   would print a *positive but wrong* residue; negative vs wrong-positive are both
   artifacts of the same missing wrap logic.)
3. 8.5 Gb/s = 1.0625×10⁹ B/s ⇒ per 60 s: 6.375×10¹⁰ B = 14.84 wraps of 2³². Δ =
   (C₂ − C₁) mod 2³² = (14.84 − 14) wraps' residue = 0.84×2³² ≈ 3.6 GB ⇒
   3.6×8/60 ≈ **481 Mb/s**... to hit the *reported* 1.1 Gb/s the residue must be
   ≈8.25 GB — that's > 2³², impossible for one residue ⇒ the reported 1.1 Gb/s
   implies the poller *did* apply some correction or clamp ⚠ (or the test's
   reported numbers include averaging). Teaching resolution: reconstruct the
   modular walk (14 wraps + residue), show the residue-only result (~481 Mb/s),
   and flag the 1.1 discrepancy as pipeline-behavior-to-verify — the audit's
   conclusion is "the numbers cannot be trusted until the pipeline is specified",
   which is the correct engineering finding.
4. Fixes: (a) poll the 64-bit OIDs (ifHCInOctets/ifHCOutOctets — HC = high
   capacity) — addresses *all* delta artifacts at 10G (wrap time at line rate
   becomes 2⁶⁴ B ÷ 1.25 GB/s ≈ 468 years — effectively never); (b) poller must
   still implement: wrap detection (delta > 2⁶³ ⇒ treat as wrap/correction) and
   counter-discontinuity tracking (sysUpTime/counter-discontinuity-time ⚠ MIB-II/
   IF-MIB semantics — on agent restart, deltas are invalid; reset the rate series);
   (c) ifSpeed (32-bit gauge caps at 4,294,967,295 b/s ≈ 4.29 Gb/s — the *port
   speed* field cannot represent 10G; ifHighSpeed (Mb/s gauge) reads 10000 ✓ —
   dashboards computing "% of link speed" from ifSpeed cap at ~43% and *display*
   ceilings that never existed. Assignment: (c) explains the 3.1 "ceiling" *if* the
   dashboard normalizes by ifSpeed; the honest reading is that each candidate
   explains a different observed number, and the audit's deliverable is the
   *test matrix*, not a single villain.

### Reasoning process
Facts: capped ifSpeed, correct ifHighSpeed, 32-bit octet counters, 60-s polls,
wrap ≈3.4 s, three inconsistent rate artifacts. Model: modular arithmetic of
counters + display-layer normalization. Audit output: artifact-by-artifact
arithmetic, unspecified-pipeline findings, 64-bit + discontinuity fix list.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "The link is bad" | The controlled test pushes 8.5 Gb/s on the same wire; the fault is in measurement |
| "Poll faster" | At 10G, even 1-s polls wrap (3.4 s at line rate... at 8.5 Gb/s ≈ 4 s) — faster polls shrink but never eliminate wrap artifacts; 64-bit counters are the fix |
| "Use ifSpeed for percent utilization" | The 32-bit gauge cannot represent 10G; percent-of-link must use ifHighSpeed |
| Trust the 1.1 Gb/s test reading | It's modular residue, not throughput — the audit's whole point |

### Extension question
Streaming telemetry (gRPC dial-out, per-second samples) replaces SNMP here. What
does it fix outright, and what *new* requirement does per-second sampling add?
(Wrap: non-issue with 64-bit counters *and* per-second deltas (residue small);
new requirement: the collector must handle 32k× the sample rate — storage,
cardinality, and down-sampling policy become the new failure surface; measurement
problems don't disappear, they move.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Modular walks per artifact with honest reconciliation; 64-bit + discontinuity + ifHighSpeed fix matrix assigned to artifacts; audit conclusion (unspecified pipeline = untrusted) |
| 3 Proficient | Wrap arithmetic right; artifact-to-fix mapping partial |
| 2 Developing | "Counter wrap" as an uncomputed slogan |
| 1 Beginning | Orders a link upgrade |

### References
- RFC 2863 (IF-MIB: ifSpeed/ifHighSpeed/ifHC* counters) ⚠ verify sections; MIB-II
  RFC 1213 (32-bit legacy) ⚠
- PD §1.4 (rate measurement) context; polling practice per vendor docs ⚠
