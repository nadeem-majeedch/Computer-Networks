# PB-010 — The Link That Passes Ping but Fails at Speed (L05, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L05 — Physical Layer: Signals, Media & Transmission Basics |
| CLOs | CLO2, CLO6 (physical-layer diagnosis from measurements) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Diagnostic (physical layer) · Topic: Physical-layer faults |
| Evidence policy | Synthetic certifier results, labeled and internally consistent; standard limits marked ⚠ |

---

## Student version

### Scenario
A new warehouse camera keeps freezing at night. The installer insists the link is fine
"because ping works." You get a cable-certifier report before anyone swaps hardware.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Certifier report (run "CAM-04"):
  Length:            118 m
  Wire map:          OK (all pairs correct)
  NEXT (pair 1-2):   marginal (4.1 dB below spec limit ⚠ value illustrative)
  Insertion loss:    high at high frequency (near limit at 250 MHz band)
Symptoms:
  ping (small packets, low rate): 100% success, <1 ms
  camera stream (~15 Mb/s):       works minutes, then macro-freeze + recovery
  ftp test file copy:             throughput collapses after ~2 min
```

### Problem statement
Explain why the link passes ping yet fails under sustained load, using the physical
measurements; identify the most likely root cause(s); and propose a fix order.

### Evidence pack
The labeled synthetic certifier report and symptom list. Treat numeric margins as
illustrative; the *pattern* (marginal NEXT + long length + speed-dependent failure) is
the evidence to reason about.

### Constraints
- Explain the ping-vs-load asymmetry mechanically (what differs on the wire).
- Do not jump to "replace the switch" — order hypotheses by evidence.
- Flag any standard-specific claims for verification ⚠.

### Student questions
1. What differs physically between a ping packet and a sustained 15 Mb/s stream on this
   run? (Name two waveform-level differences.)
2. How do 118 m length + marginal NEXT together explain the symptoms? (Why does each
   factor matter, and why *combined*?)
3. Rank hypotheses: (a) cable too long, (b) crosstalk from poor termination, (c) camera
   hardware fault, (d) switch port fault. Which does the evidence support, which does it
   not address?
4. Fix order and verification: what do you change first, and what measurement confirms
   it?

### Expected learning outcomes
- Explain why low-rate tests pass while high-rate transmissions fail on marginal links.
- Combine length (attenuation) and NEXT (crosstalk) into a coherent failure story.
- Order hypotheses by evidence rather than convenience.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Ping is rare, small, and slow. What does the transmitter do differently when it runs
   flat-out?"
2. "Two independent impairments can each be survivable alone. What does the certifier
   say about each?"

### Solution
1. Sustained streams run the transmitter at full symbol rate with continuous high-
   frequency content; pings are short bursts with idle time. Effects: more attenuation
   stress per unit time (near/far-end levels worse) and much more crosstalk coupling —
   NEXT is only painful when aggressive signals run continuously on adjacent pairs.
2. Length: 118 m exceeds the 100 m channel design point ⚠, so insertion loss is high —
   the received signal is weak, shrinking noise margin. NEXT: marginal crosstalk means
   neighbor pairs inject noise. Combined: SNR collapses under sustained load — errors →
   retransmissions → perceived freezes; at ping rates, occasional marginal symbols still
   decode, so small packets survive. Neither factor alone necessarily fails the link;
   together they do.
3. Supported: (a) length (118 m measured) and (b) termination/crosstalk (marginal NEXT,
   pair 1-2). Not addressed by this evidence: (c) camera fault and (d) switch port —
   no measurement speaks to them; they stay on the list but *after* the wire is fixed.
   Key teaching point: the certifier rules the physical layer *in or out* before
   hardware swaps.
4. Fix order: re-terminate/replace the run to ≤100 m channel with proper pairs (or
   reroute/certify a compliant run) → re-certify (length + NEXT in spec) → re-test
   sustained throughput (ftp copy for >5 min) → only then revisit (c)/(d). Confirmation:
   clean certifier pass + stable sustained transfer, not ping.

### Reasoning process
Facts: length, wire map OK, marginal NEXT, high insertion loss; symptoms rate-dependent.
Model: SNR budget = signal − (attenuation + noise); sustained load maximizes both
impairments. Hypotheses ranked by which measurements address them; fix the physical
layer first, verify with the *failing* test (sustained throughput), not the passing one.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Ping works ⇒ link fine" | Ping exercises a tiny slice of the link's operating envelope |
| Swap the camera first | Two physical measurements already point at the run; cheapest evidence ignored |
| Fix length but ignore termination (or vice versa) | The margin failure is the *sum*; one repair may not restore SNR |
| Declare 118 m "close enough" | Standards margins exist for worst-case temperature/installation variance ⚠ |

### Extension question
The same run tests perfectly in a cool morning and fails marginal re-certification in
the hot afternoon. Which impairment does temperature worsen, and what does that teach
about "passing" measurements? (Attenuation/insertion loss rises with temperature ⚠;
margins that pass at room temperature can fail in attics/roofs — measure in worst-case
conditions or insist on real margin.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Mechanical ping-vs-load explanation; both impairments combined correctly; hypotheses ranked with explicit "not addressed" honesty |
| 3 Proficient | Correct root cause; one mechanism hand-waved |
| 2 Developing | Blames crosstalk alone or length alone; no SNR-budget reasoning |
| 1 Beginning | Recommends hardware swaps immediately |

### References
- PD §2.3 (twisted pair, attenuation, crosstalk), §2.2 (SNR and capacity)
- Tanenbaum & Wetherall Ch. 2 (transmission impairments) ⚠ verify section
