# PB-021 — The Conference Room Syndrome (L11, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L11 — Wireless in Practice + LAN Security Preview |
| CLOs | CLO6 (systematic wireless troubleshooting), CLO2 (roaming/ESS mechanics) |
| In-class slot | Main activity; 20 min, groups of 3 |
| Case type | Diagnostic · Topic: Wireless networking |
| Evidence policy | Synthetic survey + ticket evidence, labeled; mechanisms per 802.11 roaming theory |

---

## Student version

### Scenario
The executive conference room is a running joke: laptops work in the doorway, drop to a
crawl at the table, and calls drop when someone closes the door. APs exist on *both*
sides of the room.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (values illustrative):**

```
Layout:   AP-3 (corridor, 15 m away, through 2 drywall walls); AP-4 (in the room,
          ceiling-mounted above the door)
Survey at the table:
  AP-3: RSSI −68 dBm, SNR 28 dB, channel 36
  AP-4: RSSI −55 dBm, SNR 38 dB, channel 36 (same channel!)
Ticket history: complaints spike during all-hands calls; fine when the room is empty
Client logs (one user): association to AP-4; then repeated "deauth/roam to AP-3"
                        events during calls; ping loss bursts 200–800 ms during roams
```

### Problem statement
Diagnose why a room with two adequate APs behaves worse than either alone, explain the
roam events with 802.11 mechanics, and produce a channel/coverage plan for the room.

### Evidence pack
The labeled synthetic survey and logs. Facts: both APs strong at the table; same
channel; roam events correlate with call quality; room occupancy correlates with
complaints. Assumptions you may need (label them): client roaming algorithm is
RSSI-threshold based (typical, but client-specific).

### Constraints
- Explain co-channel consequences *with the CSMA/CA mechanism*.
- The plan must fix roaming AND the door-closed symptom.
- No inventing of vendor features; stick to standard 802.11 behavior + labeled
  assumptions.

### Student questions
1. Why does "two strong APs, same channel" produce *worse* airtime than one?
2. Explain the observed roam events: what makes a client abandon AP-4 mid-call even
   though its signal is good, and what does each roam cost the call?
3. Door closed: which measurement changes most, and why does that break the marginal
   link (name the chain: RSSI → SNR → rate → airtime)?
4. Produce the plan: channel assignment, any power change, and what to measure to
   confirm the fix.

### Expected learning outcomes
- Diagnose co-channel interference between one's own APs as self-inflicted contention.
- Explain client-initiated roaming and its cost to real-time traffic.
- Relate physical attenuation (door) to rate collapse via SNR.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Same channel means the two APs *take turns* — including on each other's beacons and
   each other's clients' traffic."
2. "The client, not the network, decides to roam. What does a busy channel do to the
   *measured* quality that drives that decision?"

### Solution
1. Both APs share channel 36: every transmission (data, beacons, ACKs) from AP-3 and
   its clients must wait for AP-4's airtime and vice versa (CSMA/CA deferrals). The
   room's effective capacity is split *and* the overhead doubles — beacons from two
   BSSes, plus heard-but-irrelevant traffic — so per-client airtime drops despite
   "good signal" everywhere.
2. Roams: during all-hands, channel 36 is saturated; the client's measured quality
   (airtime, retransmission delays) degrades; typical RSSI-threshold/quality-hungry
   roaming logic hunts for a "better" BSS and hops to AP-3 — which is *also* on 36 and
   equally saturated. Each roam costs a deauth/reassociation gap (ping loss 200–800 ms
   is consistent with the log) — fatal to a call. (Assumption, labeled: client uses
   standard RSSI-driven roaming; exact thresholds are vendor/client-specific ⚠.)
3. Door closed adds attenuation on the AP-4 path (metal/wood door, typically 3–6 dB+
   ⚠ illustrative): RSSI drops (e.g., −55 → −61), SNR falls, the adaptive rate picks a
   slower MCS, so the *same airtime* carries fewer bits; combined with contention, the
   call collapses. The chain: attenuation → lower SNR → lower PHY rate → less data per
   airtime unit → worse effective throughput.
4. Plan: put AP-4 on a *different* clean channel (e.g., 5 GHz channel 52/100 per the
   site plan ⚠ DFS rules apply), AP-3 stays on 36; verify −55/−68 dBm separation is
   enough for stable client "best BSS" selection; optionally reduce AP-3's power so the
   corridor serves the corridor (coverage shaping). Confirm with: roam-event count
   before/after during a full room, iperf at the table, call MOS-proxy (jitter/loss
   stats) during all-hands.

### Reasoning process
Facts: same channel, both APs strong, roams correlate with calls + occupancy, door
attenuates. Model: co-channel contention (shared airtime) + client roaming dynamics +
attenuation→SNR→rate chain. Multi-cause diagnosis with labeled assumptions; plan
addresses channel plan first (root contention), power second (coverage shaping).

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Add a third AP" | Adds another contending transmitter to channel 36; makes it worse |
| "Max transmit power everywhere" | Increases overlap, contention, and sticky-client pathologies |
| "Ban laptops from the room" | Treats users as the fault; occupancy correlation was a *clue to load*, not a cause |
| "Different SSIDs per AP for control" | Kills roaming entirely; calls drop at the doorway |

### Extension question
Meridian wants *seamless* calls while walking corridor→room. Name the 802.11 mechanisms
at both ends that make roaming fast, and the design constraint that keeps them working
here. (Fast transition/PMF support on clients+APs ⚠, pre-auth/OKC on supporting stacks;
*both* APs must offer comparable quality — which is exactly what the channel plan
restores.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Co-channel mechanism explicit; roam cost quantified from logs; attenuation→rate chain complete; channel plan + verification metric |
| 3 Proficient | Correct diagnosis; roam mechanics partly hand-waved |
| 2 Developing | "Interference" invoked without CSMA/CA mechanism |
| 1 Beginning | Recommends more APs or power |

### References
- PD §7.3 (802.11 channels/association/roaming) ⚠ verify section
- Kurose & Ross §7.3; IEEE 802.11 (BSS selection is client-implemented) ⚠
