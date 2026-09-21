# PB-055 — When the Brain Blinks (L28, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L28 — Data-Plane & SDN: Programmable Networks |
| CLOs | CLO2 (control/data plane split), CLO6 (failure-mode reasoning) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Diagnostic + trade-off · Topic: SDN |
| Evidence policy | Synthetic logs, labeled; flow/miss behavior per OpenFlow-style model, vendor fail-standalone modes flagged ⚠ |

---

## Student version

### Scenario
The lab SDN (one controller, four OpenFlow switches) briefly lost its controller
connection during a reimage. Traffic mostly kept flowing — except new conversations
and one specific flow that died. After the controller returned, everything recovered
in seconds.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (illustrative):**

```
Timeline (lab SDN):
  10:00:00  controller reachable; flows installed for all active conversations
  10:03:12  controller connection lost (reimage reboot)
  10:03:12+ long-lived flow A (host1→host3, previously installed): CONTINUES
  10:03:20  NEW conversation host2→host4 (TCP SYN): FAILS (timeout)
  10:03:25  ping host2→host4: FAILS
  10:04:00  switch logs: "packet-in dropped: controller unreachable" (repeats)
  10:06:30  controller returns; host2→host4 works within ~5 s; flow A unaffected
Switch fail-mode setting: fail-standalone (vendor default ⚠ semantics vary)
```

### Problem statement
Explain which plane makes which decision (and where each lives), account for flow A
surviving while new flows died, and evaluate the fail-standalone vs fail-secure
trade-off for a *teaching* lab vs a *production* fabric.

### Evidence pack
The labeled synthetic timeline. Facts: installed flows kept forwarding; misses
couldn't reach the controller; recovery on reconnect. Assumption to label: no
reactive re-installation raced the outage.

### Constraints
- Use the control/data-plane vocabulary precisely (where does the *decision* for a
  miss live when the controller is gone?).
- The trade-off must name what each mode does with *misses* (not just "works/
  doesn't work").

### Student questions
1. During the outage, which component decides flow A's forwarding — and which
   component *would* decide a new flow's fate?
2. Why did host2→host4 fail while flow A survived? (One sentence each, using the
   planes.)
3. What does fail-standalone do with a miss? What does fail-secure do? Which is
   riskier for a production fabric carrying real user traffic, and why is that the
   *safer* choice there?
4. For the teaching lab: which mode would you choose, and what does it teach that
   the other hides?

### Expected learning outcomes
- Locate decisions in control vs data plane under normal and degraded operation.
- Explain table-miss handling and controller-dependence of new flows.
- Weigh fail-standalone vs fail-secure for different environments.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Flow A's instructions are already *in the switch's table*. Who needs to be
   consulted to follow an instruction that's already written?"
2. "A miss is a question. To whom is the question addressed when the answerer is
   offline — and what happens to the packet in each fail-mode?"

### Solution
1. Flow A: the **data plane** (local flow table) — forwarding is table lookup; no
   controller consultation occurs for installed flows. A new flow's fate: the
   **control plane** (controller) — the switch emits a packet-in (table miss) and
   waits for an installed rule or an explicit drop.
2. Flow A survived because its match→action entry was already resident; switches
   forward on their own tables. host2→host4 generated misses; with the controller
   unreachable, the question had no answerer — the switch dropped (or, per mode,
   handled locally per fail-mode) — the log line shows packet-in drops ⇒ the
   controller-dependent path.
3. Fail-standalone: on controller loss the switch degrades to *normal L2/L3
   learning-switch behavior* — a miss is handled by flooding/learning locally
   (connectivity preserved, policy lost). Fail-secure: on controller loss, misses
   are **dropped** — no new flows at all (fail-closed; policy preserved,
   connectivity sacrificed). Production default: **fail-secure** when policy
   (segmentation, ACLs) matters more than availability — silent fail-open can
   *expose* traffic that policy would have blocked (a security regression
   masquerading as resilience); availability-critical fabrics may choose
   standalone with compensating controls. Now reconcile the evidence: with
   fail-standalone, host2→host4 would likely have *worked* via ordinary L2
   learning; the observed packet-in drops and timeouts are consistent with
   **fail-secure**, not the labeled fail-standalone default. **The mode-vs-log
   contradiction is the finding** — "which mode is actually running?" is the first
   diagnostic, and students learn to read logs against configs rather than
   against labels.
4. Teaching lab: **fail-secure** — it makes the controller's role *visible* (new
   flows die without it), which is the lesson; standalone hides the controller
   behind familiar L2 behavior. (If the lab's goal is resilience engineering rather
   than SDN basics, the choice flips — say which goal you're serving.)

### Reasoning process
Facts: installed-flow survival, miss failures, packet-in drops, mode label. Model:
plane ownership per decision type; miss handling per fail-mode. Diagnosis: reconcile
the label against observed behavior — the mismatch is the finding.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "The network was down" | Flow A crossed the same fabric the whole time |
| "The controller caches everything" | The *switch* holds flows; the controller authors them — attribution error |
| "Fail-secure is obviously safer" | Safer for *policy*, not for *availability*; the trade-off is the answer, not a slogan |
| "SDN is fragile because of this" | Traditional networks have equivalent failure modes (control-plane adjacency loss); the difference is *visibility* |

### Extension question
The vendor documents "proactive flow installation" as a mitigation. What would you
pre-install to make host2→host4 survive the next outage, and what SDN capability do
you *lose* by pre-installing broadly? (Pre-install L2/L3 reachability flows for
known endpoints — they survive outages like flow A did. Lost: reactive policy,
per-flow visibility, and the controller's ability to *change* paths mid-flight —
the flexibility that justified SDN in the first place; the trade-off is the point.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Plane attribution per decision; miss handling per mode; catches the mode-vs-log contradiction; environment-conditional trade-off |
| 3 Proficient | Planes and modes right; contradiction unnoticed |
| 2 Developing | "Controller down = network down" |
| 1 Beginning | Restarts the controller first |

### References
- PD §5.4–5.5 (SDN: control/data separation, APIs) ⚠ verify section mapping
- Kurose & Ross §5.5 (SDN context); OpenFlow spec (fail modes) ⚠ verify version
