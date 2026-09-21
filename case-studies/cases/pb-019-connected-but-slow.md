# PB-019 — Full Bars, Empty Pipe (L10, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L10 — Wireless Networking: Wi-Fi Fundamentals |
| CLOs | CLO2 (802.11 service set model), CLO6 (evidence-based wireless reasoning) |
| In-class slot | Closing consolidation; 12 min, pairs |
| Case type | Conceptual diagnostic · Topic: Wireless networking |
| Evidence policy | Synthetic survey data, labeled; PHY-rate relationships standards-consistent, values illustrative |

---

## Student version

### Scenario
Users in the analytics bullpen complain the Wi-Fi is "broken". The help desk's standard
line — "you have full bars" — doesn't satisfy the data-science students pulling 2 GB
datasets. A survey of the bullpen:

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (values illustrative):**

```
Survey (bullpen desk area):
  Signal (RSSI):        −52 dBm  (strong)
  AP:                   "MERIDIAN-2G" on 2.4 GHz, channel 6
  Neighbor networks:    11 other networks visible; 7 on channel 6 or overlapping
  Current PHY rate:     72 Mb/s (link adapts down under load)
  Measured throughput:  4–8 Mb/s during complaint hours; 25 Mb/s at 6 a.m.
  5 GHz AP ("MERIDIAN-5G"): visible from the same desks, RSSI −67 dBm, 3 neighbors
```

### Problem statement
Explain why strong signal coexists with poor throughput, identify the dominant cause
from the evidence, and recommend which network users should join and why.

### Evidence pack
The labeled synthetic survey. Facts to respect: RSSI is strong; time-of-day pattern
exists; the 5 GHz SSID is *visible* (so it's not a coverage problem).

### Constraints
- Explain the signal-strength vs throughput distinction mechanically.
- Use the time-of-day evidence; don't invent interference sources.

### Student questions
1. What does RSSI measure, and why doesn't it promise throughput?
2. Why does 11 visible networks on/around channel 6 hurt — describe the shared-medium
   mechanism.
3. Compare the two APs for these desks: coverage vs contention. Which should users pick?
4. The 6 a.m. datapoint: what does it prove, and what does it rule out?

### Expected learning outcomes
- Separate link quality (RSSI/SNR) from airtime contention.
- Explain 2.4 GHz channel overlap and CSMA/CA contention with neighbors.
- Use a time-of-day datapoint to discriminate causes.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Bars measure how well *you* hear the AP. Throughput needs *airtime* — who else is
   talking on that channel?"
2. "Two Wi-Fi networks on the same channel don't collide — they *take turns*. What
   happens to your turn when seven neighbors wait too?"

### Solution
1. RSSI = received signal power from *your* AP. It predicts link quality/possible PHY
   rate, but throughput depends on airtime availability: how much of the shared channel
   you get to use.
2. Wi-Fi is CSMA/CA: stations (including other networks' stations) must sense the
   channel idle before transmitting. Co-channel/overlapping networks force deferrals
   and backoffs; the channel is shared *between networks* — your AP can only transmit
   when everyone else stays quiet. More networks on the channel = smaller share.
3. 2.4 GHz AP: stronger signal but a crowded channel (7 co-channel/overlapping). 5 GHz:
   weaker (−67 dBm is still workable ⚠ thresholds vary by PHY) but only 3 neighbors and
   wider/cleaner spectrum. For *throughput* at these desks, 5 GHz wins despite fewer
   bars. Roaming note: same ESS naming would let devices pick; here the SSIDs differ,
   so users must choose.
4. 6 a.m. throughput (25 Mb/s) with the same RSSI proves the *link* is capable —
   rules out distance/coverage/antenna as the cause, and points squarely at
   contention/load during busy hours.

### Reasoning process
Facts: strong RSSI, crowded 2.4 GHz, visible clean 5 GHz, time-of-day dependence.
Model: throughput = PHY rate × airtime share; contention sets airtime. Cause selection:
contention (not coverage). Recommendation: 5 GHz. Discriminating evidence: off-peak
measurement.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Full bars = full speed" | Bars ≠ airtime; contention invisible to RSSI |
| "The AP is broken" | Off-peak performance proves otherwise |
| "5 GHz is faster because the number is bigger" | Here it's *less contention*, not an inherent rate advantage — justify with evidence |
| Blaming the client's antenna | Same client flies at 6 a.m. |

### Extension question
MERIDIAN-2G and MERIDIAN-5G have different names. What breaks for a roaming user with a
single "MERIDIAN" expectation, and what does a proper ESS design do instead? (Different
SSIDs = different service sets; roaming is manual. A proper design uses one SSID across
both bands so the *client* steers bands — discuss sticky-client caveats.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Airtime mechanism explicit; 5 GHz justified by contention not vibes; 6 a.m. datapoint used to exclude coverage |
| 3 Proficient | Correct cause + recommendation; mechanism partially stated |
| 2 Developing | Equates RSSI with throughput |
| 1 Beginning | "Restart the AP" |

### References
- PD §7.3 (802.11: CSMA/CA, channels, architecture) ⚠ verify section numbering
- Kurose & Ross §7.3 (WiFi: 802.11 architecture/MAC)
