# PB-059 — Married to the Wrong AP (L30, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L30 — Mobile & Wireless Enterprise Networking |
| CLOs | CLO2 (cell selection/roaming), CLO6 (evidence-based wireless reasoning) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Diagnostic-conceptual · Topic: Wireless networking |
| Evidence policy | Synthetic survey data, labeled; stickiness behavior client-implemented ⚠, values illustrative |

---

## Student version

### Scenario
Fourth-floor users beside the new AP-9 complain of poor video quality — while sitting
directly under it. The survey shows their laptops associate to AP-3, two floors down.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (values illustrative):**

```
User position:  3 m from AP-9 (same floor)
Survey:
  AP-9: RSSI −48 dBm, channel 149, load ~15%
  AP-3: RSSI −71 dBm, channel 36, load ~60% (three floors of busy offices)
Laptop association: AP-3 (confirmed on 6 of 8 laptops)
AP-3/AP-9: same SSID "MERIDIAN", same ESS — roaming is *supposed* to happen
Laptop logs: "association to AP-3 retained; roam threshold not reached"
AP-9 deployed last week; laptops have not been rebooted since
```

### Problem statement
Explain why healthy clients "stick" to a weaker, busier AP, why deployment order
matters here, and what mechanism (client-side or network-side) fixes this class of
problem.

### Evidence pack
The labeled synthetic survey. Facts: RSSI/load deltas, same ESS, roam threshold not
reached, laptops older than the AP deployment. Assumption to label: standard
client-driven roaming (no vendor fast-roaming in play ⚠).

### Constraints
- Explain stickiness as client *policy*, not client *defect*.
- The fix must work for the 6 laptops *without* manual per-device config.

### Student questions
1. What is the client's roaming decision actually optimizing (per standard 802.11
   behavior), and why is −71 dBm "good enough" for it?
2. Why do 6 laptops all show the same behavior? (What do they share?)
3. Two fix classes: (a) network-side — make AP-3 less attractive (power/channel
   planning); (b) client-side — force re-evaluation. What does each do, and which
   fixes the *class* vs the *instance*?
4. The 2 laptops that did roam: what does their behavior prove about the design?

### Expected learning outcomes
- Explain client-driven cell selection and stickiness.
- Tie deployment order (AP appears after clients associate) to stale behavior.
- Distinguish per-instance fixes from coverage-design fixes.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Roaming is the *client's* choice, made when *its* thresholds are crossed. What
   does −71 dBm look like to a threshold set for 'don't roam until it's terrible'?"
2. "The laptops are older than the AP. What has every laptop's radio decided *once*
   and never re-decided since?"

### Solution
1. Clients roam when measured quality drops below *their* internal thresholds (RSSI
   floors, retry rates) — a policy protecting against ping-pong, not optimizing
   load. −71 dBm is well above typical roam-away thresholds (often −75 to −80 ⚠
   client-specific), so AP-3 stays "acceptable" — and the client has no idea AP-9
   (−48 dBm) exists as a *better* option unless it scans and re-evaluates.
2. Shared behavior: same OS/driver, same SSID association made *before AP-9
   existed* — all six associated to AP-3 when it was the only/best choice and never
   re-triggered a scan-reassociate (idle clients scan lazily; association is
   sticky). Not coincidence — shared policy and shared history.
3. (a) Network-side: reduce AP-3's coverage on floor 4 (lower transmit power,
   channel plan) so clients *measure* AP-3 as marginal → thresholds crossed → roam.
   Fixes the class for *every* client, present and future — but is coarse (affects
   AP-3's legitimate coverage on floors 2–3; design the plan, don't just turn it
   down). (b) Client-side: force a reconnect/disconnect cycle per device — fixes 6
   instances, nothing else, and recurs for every future visitor. Class fix = (a)
   with (b) as the immediate unblock; the honest answer uses both.
4. The 2 laptops that roam prove the ESS design itself works (same SSID, roam
   possible, AP-9 healthy) — the fault is in *trigger conditions*, not in the
   architecture. Diagnosis by exception: working instances bound the fault.

### Reasoning process
Facts: RSSI/load contrast, same ESS, sticky associations predating AP-9, two
counter-examples. Model: client-threshold roaming + lazy rescans. Class-vs-instance
split: design fix (coverage shaping) vs operational unblock (reassociation).

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "AP-9 is broken" | −48 dBm at 3 m is excellent; two clients roam to it fine |
| "Ban AP-3" | Removes needed coverage on floors 2–3; coverage is designed, not deleted |
| "Tell users to forget the network" | Per-user toil; recurs for every new device; a workaround wearing a fix's clothes |
| "More power to AP-9" | Worsens co-channel contention (PB-021's lesson) and overshoot into neighboring floors |

### Extension question
Meridian adds 802.11k/v/r (radio measurement / BSS transition / fast transition ⚠).
Which of these *lets the network* tell the client "move to AP-9", and why is it still
not a guarantee? (802.11v BSS Transition Management lets the AP *request* a roam —
clients may refuse (it's advisory, not mandatory); 802.11r speeds the *handover*
once a roam happens; 802.11k gives the client neighbor reports to scan smarter.
Networks suggest; clients decide — the asymmetry is the point.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Client-policy mechanism; shared-history explanation; class-vs-instance fixes with honest trade-offs; counter-example bound reasoning |
| 3 Proficient | Correct diagnosis; fixes not separated by scope |
| 2 Developing | "Bad AP" or "bad laptops" |
| 1 Beginning | Reboots everything |

### References
- PD §7.3 (802.11 architecture/mobility) ⚠ verify section mapping
- Kurose & Ross §7.3; IEEE 802.11k/v/r ⚠ (client-implemented roaming asymmetry)
