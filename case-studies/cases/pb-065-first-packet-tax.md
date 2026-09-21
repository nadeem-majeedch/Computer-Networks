# PB-065 — The First-Packet Tax (L28, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L28 — Data-Plane & SDN: Programmable Networks |
| CLOs | CLO5 (latency arithmetic), CLO6 (reactive-vs-proactive trade-off) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Calculation + trade-off · Topic: SDN |
| Evidence policy | Synthetic measurements, labeled; miss-path arithmetic per OpenFlow-style model; internally consistent |

---

## Student version

### Scenario
The lab SDN fabric uses *reactive* flow installation: the first packet of every new
flow goes to the controller, which computes a path and installs rules. The dashboard
shows healthy switch CPU and controller RTT — yet users notice the first page load
after each login "hangs".

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (illustrative values):**

```
Controller RTT (switch↔controller): 5 ms (measured, stable)
Miss handling:                      first packet buffered; rule installed on reply
A typical dashboard page load:      ~250 ms total, 12 new flows to 12 distinct
                                    destinations (CSS, JS, API endpoints…)
Subsequent loads:                   flows cached in switches → no misses
P95 page load (first load):         ~370 ms; subsequent: ~255 ms
DNS flows:                          also miss (new 5-tuples per resolver query)
```

### Problem statement
Model the first-packet tax (which packets pay the 5 ms, and how many times per page),
reconcile the observed 370 ms, and evaluate reactive vs proactive vs hybrid
programming for this workload.

### Evidence pack
The labeled synthetic measurements. Facts: 12 new flows per first load, 5 ms miss
round-trip, P95 delta ≈115 ms. Assumptions to state: misses processed serially per
switch ingress (teaching model), no controller queuing.

### Constraints
- The 115 ms delta must decompose into miss-count × cost (+ anything you add,
  labeled).
- The recommendation must handle *both* the first-load spike and the long-tail of
  rare destinations (why pure proactive doesn't win outright).

### Student questions
1. Which packets pay the tax in this design — every packet, every flow, or the
   first packet of each flow? What does the *switch* do while waiting?
2. Arithmetic: 12 flows × 5 ms = 60 ms of the observed 115 ms delta. Propose the
   remaining ~55 ms with labeled candidates (DNS miss path? parallel vs serial
   misses? TLS setup?).
3. Pure reactive: what happens to the P95 for a user who visits a *rare* internal
   tool (all 15 flows new)? Pure proactive (all pairs pre-installed): what breaks
   when the fabric has 50 switches and 2,000 endpoints?
4. Hybrid design: which flows get pre-installed, which stay reactive, and what
   triggers promotion from reactive to proactive?

### Expected learning outcomes
- Attribute latency to control-plane round trips on the miss path.
- Decompose measured deltas into labeled components.
- Design hybrid flow programming with explicit promotion criteria.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "The switch forwards at line rate for flows it *knows*. For flows it doesn't —
   where does the first packet wait, and for how long?"
2. "60 of the 115 ms is explained by data-flow misses. What *else* is a flow in an
   SDN fabric? (Hint: the resolver conversation is one.)"

### Solution
1. Only the **first packet of each flow** pays: it's buffered at the switch
   (packet-in → controller → flow-mod → packet-out), then the flow runs at line
   rate. Subsequent packets never see the controller.
2. 60 ms (12 data-flow misses). Remaining ~55 ms candidates (each must be labeled
   as hypothesis): (a) DNS misses — the resolver conversation adds 1–2 new flows
   (and possibly per-query 5-tuples if source ports vary ⚠ — that could add
   several more misses); (b) TCP handshake packets themselves are the *first*
   packets of the data flows — the SYN waits the full 5 ms, and the handshake's
   RTT inflation serializes: each flow's SYN + 5 ms inflates connection setup,
   and page loads open connections *sequentially* when the browser discovers
   dependencies (CSS → fonts → API) — the serial chain multiplies the tax; (c)
   controller processing time (rule computation) on top of RTT ⚠ unmeasured here.
   The honest decomposition: 60 ms proven + ~55 ms plausible-but-unproven — the
   audit step is to count packet-in events per load (the switch log says exactly
   how many misses happened).
3. Rare tool: all 15 flows miss ⇒ +75 ms+ (worse proportionally — small loads pay
   a bigger *percentage*). Pure proactive at 50 switches × 2,000 endpoints:
   rule-space explosion (per-pair rules ≈ switch pairs × endpoints² in the worst
   design), installation storms on topology changes, and stale rules after moves
   — the scale ceiling that motivated reactive in the first place.
4. Hybrid: pre-install the *hot, predictable* set (default gateway pairs, resolver,
   core services — a bounded list per PB-026-style addressing plan); keep reactive
   for the long tail; promote reactive→proactive after N hits in M minutes
   (e.g., ≥10 hits/5 min — the switch's counters already have this data), with a
   TTL to demote stale promotions. This bounds controller load AND caps the
   first-packet tax for the flows users actually repeat.

### Reasoning process
Facts: 5 ms RTT, 12 new flows, Δ115 ms P95, subsequent loads clean. Model: miss =
one RTT + rule install; tax is per-flow-first-packet. Decompose proven vs
hypothesized components; evaluate the three programming models against the
workload's shape (many repeated flows, long rare tail) ⇒ hybrid with counter-driven
promotion.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "SDN is slow" | Subsequent loads: 255 ms ≈ baseline — the tax is first-contact only, and it's a *design choice*, not an inherent cost |
| "Pre-install everything" | Rule-space and churn at 50 switches make pure proactive unmanageable — the scale wall the question asks you to hit |
| "Reduce controller RTT to 1 ms" | Shaves 48 ms off the *proven* component but leaves the serial-dependency inflation and DNS misses; also 1 ms RTT to a controller isn't a config knob ⚠ — it's a placement decision |
| Blame the browser | The browser's dependency-serial behavior is normal; the fabric's miss tax is what turns it into 115 ms |

### Extension question
The team proposes *packet-out pacing*: the controller replies to misses for the 12
flows in parallel. Which component of your decomposition does that collapse, and
which survives? (Parallel handling collapses the *serial-miss* portion of the 60 ms
(12 sequential RTTs → ~1 RTT of controller time) — but each flow's SYN still waits
its own 5 ms and the dependency chain's *connection-serialization* survives; the
P95 delta shrinks to roughly the handshake-inflation remainder. Predict: Δ ≈ 40–60
ms remains ⚠ — then verify by counting packet-in timings, not by trusting the
model.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Per-flow-first-packet model; 60/115 decomposition with labeled hypotheses; scale-wall answer for pure proactive; hybrid with concrete promotion criteria |
| 3 Proficient | Model and arithmetic right; hybrid criteria vague |
| 2 Developing | "Reactive adds latency" without the per-flow structure |
| 1 Beginning | Blames the controller hardware |

### References
- PD §5.5 (SDN control paradigms: reactive vs proactive) ⚠ verify section mapping
- Kurose & Ross §5.5 (SDN context); OpenFlow spec (packet-in/flow-mod) ⚠ verify
