# PB-016 — The MAC Address That Couldn't Sit Still (L08, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L08 — Switching & LAN Design |
| CLOs | CLO2, CLO6 (diagnose loops/flapping; evaluate remedies) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Diagnostic · Topic: Ethernet and switching |
| Evidence policy | Synthetic CAM/log evidence, labeled; mechanism per learning-switch + loop theory |

---

## Student version

### Scenario
Every so often, the lab NAS "disappears" for 30–90 seconds: pings fail, then everything
is normal again. No reboot logs on the NAS. You get switch evidence for one incident
window.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Switch log (one incident):
  14:02:11  MAC flapping: aa:bb:cc:00:11:22 (NAS) moves Gi0/3 → Gi0/7
  14:02:12  MAC flapping: aa:bb:cc:00:11:22 moves Gi0/7 → Gi0/3   (repeats ×40 in 60 s)
  14:02:15  %LINK-3-UPDOWN: Gi0/7 changed state to up            (was up at 14:01:58)
  14:03:40  no further flapping; NAS reachable
During incident: broadcast volume ≈ 30× baseline (measured on the monitor port)
Port Gi0/7: a cable labeled "to print server" (device unpowered for months)
```

### Problem statement
Diagnose the outage. Explain the flapping mechanism frame-by-frame, why the NAS (not the
print server) is the victim, and why broadcasts exploded.

### Evidence pack
The labeled synthetic log. Facts: Gi0/7 came up seconds before the flapping; the print
server is unpowered; nothing on the NAS itself changed. Assumptions must be labeled.

### Constraints
- Explain causality: what came *up* first, and what followed.
- Propose the fix(es) and say which also protects against the next incident.

### Student questions
1. Sequence the events: what happened at 14:01:58 and why did it start the incident?
2. Frame-level: how does a loop make one MAC appear on two ports alternately?
3. Why did broadcasts multiply ~30×, and why does that scale with the number of switches?
4. Two fixes: (a) unplug Gi0/7, (b) enable loop prevention (e.g., STP/loop guard). Which
   stops *this* incident, which stops the *next* one, and what does each NOT protect?

### Expected learning outcomes
- Diagnose a physical loop from CAM flapping + broadcast amplification.
- Explain broadcast storms as positive feedback across multiple switches.
- Weigh immediate remediation vs structural protection.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "A port that shouldn't be live just came up. What two ends does its cable connect?"
2. "Follow one broadcast frame around the loop. Does it ever die?"

### Solution
1. At 14:01:58 Gi0/7 came up. If the "print server" cable's far end plugs back into the
   same LAN (e.g., into another switch or wall port), the link creates a **loop**:
   frames can circulate. (Hypothesis, labeled: cable patch connecting the network to
   itself; consistent with an unpowered endpoint.)
2. In a loop, each switch re-learns the NAS MAC from copies arriving on *different*
   paths: a frame from the NAS enters via Gi0/3, circulates the loop, and re-enters via
   Gi0/7; the learning rule overwrites the entry — flap. Every subsequent frame to the
   NAS may then be flooded out the wrong port (or both), feeding the storm.
3. Broadcasts never terminate: each switch floods them out all ports except the arrival
   port; with a cycle, copies loop forever, and each pass re-floods on all other
   switches — multiplicative growth until the fabric saturates (30× measured is
   plausible for a small loop; exact multiplier depends on topology — labeled).
4. (a) Unplug stops *this* incident instantly (loop broken). (b) Loop prevention (STP
   blocking one loop port, or loop-guard/BPDU-guard on edge ports) stops the *next*
   one automatically. Neither protects against: unicast flooding from MAC table
   exhaustion, or loops that include devices that don't speak STP — layer the controls.

### Reasoning process
Facts: port-up event precedes flapping; single MAC alternating ports; broadcast
amplification; unpowered label device. Model: loop → re-learning oscillation + infinite
broadcast circulation. Causal chain: link-up → loop → flap+storm → outage. Fix now,
protect structurally.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "The NAS NIC is failing" | Flapping is *between ports*; a failing NIC can't be in two places |
| "Reboot the switch" | Loop persists after reboot; incident recurs |
| "Broadcast storm = too many broadcasts, so rate-limit" | Treats symptom; the loop is the source; rate-limiting can *hide* future loops |
| Blaming DHCP/IP conflicts | L2 phenomenon; IPs never entered the evidence |

### Extension question
The same symptom (MAC flapping) can occur **without** a loop: give one benign and one
malicious cause, and name the additional evidence each would show. (Benign: active/
standby NIC teaming moving the MAC between ports — planned, low rate, logged
maintenance. Malicious: MAC-spoofing attack — one port, no storm, paired with odd
traffic patterns; distinguishes by *rate* and *topology knowledge*.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Causal sequence correct; flap mechanism at frame level; storm growth explained; fixes layered with honest non-protection scope |
| 3 Proficient | Diagnoses loop; mechanism partly vague |
| 2 Developing | Blames the NAS or the "print server" device |
| 1 Beginning | Reboots equipment |

### References
- PD §6.4 (switch learning; flooding), §6.4.3 (SP: 802.1D spanning tree context)
- Kurose & Ross §6.4.3–6.4.4 (self-learning; broadcast storms framing)
