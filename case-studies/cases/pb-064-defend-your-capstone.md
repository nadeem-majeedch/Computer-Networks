# PB-064 — Defend Your Capstone (L32, Expert)

| Field | Value |
|---|---|
| Difficulty | **Expert** |
| Lecture(s) | L32 — Capstone Workshop, Presentations & Course Synthesis |
| CLOs | CLO6 (design defense under challenge), CLO3 (security/trade-off articulation) |
| In-class slot | Capstone clinic; 35 min, teams of 3–4 (rotating board) |
| Case type | Synthesis + adversarial defense · Topic: Enterprise design (capstone integration) |
| Evidence policy | Synthetic capstone briefs + board questions, labeled; multiple defensible answers exist; the graded skill is *reasoned defense*, not a "correct" design |

---

## Student version

### Scenario (capstone defense format)
Each team's capstone is a two-building campus design (HQ-A + HQ-B + warehouse) built
across the semester. In this exercise, your design faces the *board*: other teams,
armed with the question bank below, attack your choices. Your team must defend,
concede gracefully where the evidence demands, and document residual risk honestly.

**Synthetic evidence — prepared for this case; the brief your team receives:**

```
Your capstone design (as submitted):
  D1  Inter-building: one 10 Gb/s fiber (HQ-A↔HQ-B) + old 1 Gb/s retained as
      emergency path (PB-062's recommendation)
  D2  Segmentation: per-function VLANs (staff/analytics/IoT/printers/warehouse),
      VLSM plan from 10.20.96.0/19 (PB-026's corrected plan)
  D3  Wireless: single SSID, band-steered, 5 GHz-priority channel plan (PB-021's
      lessons); guest network on isolated VLAN with L3-ACL egress (PB-022's
      interim design)
  D4  Services: DHCP snooping + DAI on access VLANs; 802.1X *deferred* to
      "phase 2 — pending budget" (PB-052's fallback posture)
  D5  Monitoring: event-based link/syslog alerting + two-vantage synthetic probes
      for the analytics path (PB-056/057's design)
Board question bank (each team gets 4, drawn from):
  Q1  "Your D1 emergency path: what fails *silently* if the 10 G link dies and
       the 1 G path can't carry the analytics load? Where's the alarm?"
  Q2  "D2: the IoT VLAN has 200 devices and no 802.1X. Walk me through A3-style
       identity spoofing from the warehouse — what stops it, exactly?"
  Q3  "D3: guest VLAN egress is an L3 ACL. Name the control that fails open if
       the ACL is deleted in error — and your compensating detection."
  Q4  "D5: your probes run from two vantage points. Which failure mode is *still
       invisible* to your entire monitoring design?"
  Q5  "Across the whole design: name your single riskiest deferred decision and
       the trigger that should escalate it."
```

### Problem statement
Prepare the defense: for each board question, give (a) the direct answer with
mechanism, (b) the residual risk you concede, and (c) the compensating control or
escalation trigger. Then write your "top riskiest deferred decision" memo (Q5) —
one page, CFO-readable.

### Evidence pack
Synthetic evidence — prepared for this case; internally consistent; not from a live
system. The board's questions are *earned* —
each targets a real gap your design inherited from a prior case's honest fallback.
No invented products; defenses must be mechanisms already taught (or honestly
conceded as absent).

### Constraints
- Every answer must name the *mechanism* (a protocol/control from the course), not
  a product or a promise.
- Concessions are graded positively: a defense that claims coverage where none
  exists scores worse than an honest residual-risk statement.
- Q5's memo must be decidable: trigger → action → owner, in CFO language.

### Student questions
1. Q1: what fails silently, and what alarm would you add (mechanism + vantage)?
2. Q2: enumerate what *does* stop warehouse-side identity spoofing today (posture
   D4), and what doesn't — then state the phase-2 trigger.
3. Q3: which control fails open, and what detection catches its deletion within
   minutes (not days)?
4. Q4: name the invisible failure mode and the *class* of probe that would cover it.
5. Q5 memo: your pick, trigger, action, owner — four lines.

### Expected learning outcomes
- Defend design decisions with mechanisms and honest residuals.
- Identify fail-open vs fail-closed behavior in one's own design.
- Write escalation-ready risk statements for non-technical audiences.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "The board questions are mirrors: each reflects a fallback your design chose
   when a control was 'deferred'. Defense = mechanism + concession + trigger."
2. "Q4 is the deepest: your probes share a property with everything they monitor.
   Name the shared property."

### Solution (strong answers; teams may differ defensibly)
1. **Q1:** Silent failure: the analytics load, exceeding 1 Gb/s, degrades to
   window-bound crawl (PB-006) — *connectivity stays green* while R1's 30-min
   transfers quietly blow to hours. Alarm: per-flow *SLO probe* — a scheduled
   synthetic 1 GB transfer between buildings with an alert on completion-time
   (not link state): mechanism = throughput SLO probe from the analytics subnet
   vantage (PB-056's presence/absence logic, upgraded to *performance* absence).
   Concede: until installed, only user complaints detect it — state the residual
   in the memo.
2. **Q2:** Today's stops: DAI/snooping (if the feature survey passed ⚠) blocks
   ARP spoofing *on access ports*; the L3 boundary (ACLs between IoT and
   grade-DB VLANs) blocks routed access; the corrected VLSM plan keeps IoT in
   its own prefix (PB-026) so one spoofed identity can't cross subnets silently.
   What doesn't stop it: *within-IoT-VLAN* spoofing (DAI bindings from DHCP
   cover only leased addresses — statically configured warehouse devices can
   contest each other; PB-024's mechanism lives at small scale), and 802.1X
   port-auth is absent (anyone with a warehouse port is "trusted"). Trigger for
   phase 2: IoT VLAN device count × site incidents, or first confirmed
   within-VLAN spoof — whichever first; owner: network lead.
3. **Q3:** Fail-open control: the L3 ACL egress for guest VLAN — deletion (or a
   config rollback, PB-049's documented-vs-running lesson) leaves guests routed
   with the *default* posture of the L3 switch; if the switch's default is
   permit, guests gain internal reachability silently. Compensating detection:
   config-diff alerting (syslog/SNMP on config changes ⚠ + a nightly
   *behavioral* probe from the guest VLAN: attempt a connection to the grade DB
   and alert on *success* — the negative probe; PB-056's pattern inverted).
   Concede: real-time prevention absent; minutes-scale detection is the design.
4. **Q4:** Invisible failure: anything wrong *at or beyond the probes' own shared
   dependency* — e.g., both vantage points ride the same internet edge/ISP for
   their transit (or both depend on the same DNS resolver): a failure there
   silences the probes *and* the metrics together (PB-056's quorum logic detects
   vantage-death only if vantages are truly independent — check the dependency:
   shared resolver, shared uplink, shared power?). Class of probe: dependency
   audit + out-of-band probe (a third vantage on a genuinely independent path —
   e.g., LTE/5G dongle probe ⚠ cost — or accept and document the shared-
   dependency residual). The teaching point: monitoring systems inherit the
   failure modes of their own dependencies.
5. **Q5 memo (model):** *Riskiest deferred decision: 802.1X port authentication
   (D4, phase 2).* Trigger: warehouse occupancy > 50 unmanaged devices, OR any
   confirmed spoof incident, OR Q2's survey confirming missing DAI. Action:
   fund phase 2 (EAP-TLS with MAB fallback for printers — PB-052's survey plan);
   interim owner: network lead; board owner: CFO. Residual while deferred:
   within-VLAN spoofing and rogue-device admission are *possible*; detection
   (flap alarms, negative probes) limits dwell time, not admission.

### Reasoning process
Method: question → mechanism answer → concession → trigger. The defense's
integrity comes from the course's own honest-fallback trail (each deferred control
was documented with its gap); the board attacks exactly those seams. Q5 forces
prioritization across all residuals — the synthesis of synthesis.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "We'd add more monitoring everywhere" | Monitoring without named mechanisms/vantages is a promise; Q1/Q3 answers need probe *designs* |
| "802.1X will be added soon" (as a full answer) | 'Soon' is not a trigger, owner, or action — Q5 exists to convert intentions into decisions |
| "That risk is acceptable" (without residual documentation) | Acceptance is an *act* (PB-052's D4: risk acceptance in writing) — undocumentable acceptance is avoidance |
| Defending every question to the death | The rubric rewards honest concession; a false coverage claim is the worst outcome (and the board is instructed to probe for exactly that) |

### Extension question
The board asks the *instructor*: "which capstone decision would you un-defer first if
the budget doubled?" — answer it yourself for your design, and justify against your
Q5 memo. (Trains the meta-skill: the same trigger/action/owner logic applied by the
*designer* to their own risk register; there is no single right answer — the grading
is the reasoning quality.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Mechanism-backed answers with honest concessions on all four board questions; Q5 memo decidable (trigger/action/owner); Q4's shared-dependency insight |
| 3 Proficient | Solid defenses; concessions generic; memo lacks a trigger |
| 2 Developing | Defends with products/promises; claims coverage where deferred |
| 1 Beginning | Restates the design |

### References
- Course case bank (defense materials): PB-006, PB-021, PB-022, PB-024, PB-026,
  PB-050, PB-052, PB-056, PB-057, PB-062
- PD §8 (security architecture) ⚠ verify section mapping
