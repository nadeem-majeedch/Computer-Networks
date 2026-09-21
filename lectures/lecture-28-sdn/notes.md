# Lecture 28 — Instructor Teaching Notes
## Data-Plane & SDN: Programmable Networks (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO6 primary; CLO2 architecture thread |
| Textbook anchor | PD §4.3 (SDN sections); OpenFlow paper (⚠ verify citation) |

---

## 1. Objectives hook
Board: **"For 30 years, every switch decided alone. SDN asks: what if one brain
could see the whole network?"**

Hook (2 min): the L08 demo replayed — but this time, the FDB isn't the switch's
memory, it's a *table the controller writes*. Students recognize the shape;
that recognition is the lecture's opening bet.

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–5 | Recap + hook | L16/L27 recall; the replayed L08 demo |
| 5–18 | Concept 1 | Planes: control vs data vs management |
| 18–40 | Concept 2 | SDN architecture: controller, southbound (OpenFlow), northbound |
| 40–52 | Concept 3 | Flow tables: match-action model, priorities, timeouts |
| 52–58 | GA-28 briefing | — |
| 58–63 | Break | — |
| 63–95 | GA-28 (write rules) | Pairs write rules for reachability + policy |
| 95–110 | Findings | Two pairs read their rules; class critiques |
| 110–117 | Summary + exit ticket | — |
| 117–120 | Bridge to L29 (monitoring) | How would you *see* flow-table hits? Teaser for operations |

## 3. Concept walkthrough

### 3.1 Planes (13 min)
- **Data plane:** per-packet forwarding — the L02 "does the work" line.
- **Control plane:** decides *what* the data plane does (routing algorithms,
  L08 learning) — "decides the work."
- **Management plane:** configuration and monitoring (VLAN policy, SNMP) —
  "tells the worker the rules."
- Anchor examples: OSPF recalculation = control; frame out port 3 = data;
  operator sets VLAN = management. Students sort 6 examples (activity).

### 3.2 SDN architecture (22 min)
- **Separation:** control logic moves out of devices into a logically
  centralized controller; devices become forwarding elements.
- **Southbound interface:** controller ↔ switches (OpenFlow is the classic
  protocol; teach the *interface idea*, name OpenFlow, don't enumerate its
  message types).
- **Northbound interface:** controller ↔ applications/policy (invented per
  deployment; no standard to cite — say so).
- **Controller consistency:** logically centralized ≠ one machine; replicas
  and partitions exist (one honest sentence).
- **The match-action abstraction:** a flow rule = (match on header fields) →
  (actions: forward/drop/modify); priority orders overlapping rules; counters
  and timeouts give observability — the same table shape students met in
  L25's nftables chains, now programmable from software.

### 3.3 Flow tables in practice (12 min)
- Rule lifecycle: controller installs → switch matches packets in priority
  order → counter increments → idle timeout evicts (or hard timeout).
- **Reactive vs proactive:** controller installs on first packet (learning-
  switch style) vs pre-installed policy. Students connect reactive to L08's
  learning behavior — the same algorithm, relocated.
- **Pipeline note:** OpenFlow supports multi-table pipelines in switches;
  teach single-table, name the pipeline honestly (one sentence).

### Reference diagram — Controller programs the data plane

```text
controller ──"match dst=10.0.0.9 → port 3"──→ switch flow table
 table-miss ──→ PACKET-IN ──→ controller decides ──→ rule installed
 after install: packets take the fast path without the controller
```

## 4. Important definitions
Control plane · Data plane · Management plane · SDN controller · Southbound
interface · OpenFlow (named) · Northbound interface · Flow table · Match-action
rule · Priority · Reactive vs proactive installation · Idle/hard timeout.

## 5. Real-world examples
- **Google B4 / data-center fabrics** (named as the canonical deployments —
  ⚠ cite the paper if you assign it).
- **Data-center overlays and virtual networks** from L27 are SDN applications:
  the "API-controlled VLAN" from last lecture *is* the northbound story.

## 6. Mathematical/technical example
GA-28 rule-writing on a trace: given topology H1—S1—S2—H2 and the packet trace
`H1:eth0 → S1:port1`, students write the reachability rule. Match fields:
`in_port=1, eth_type=ip, ip_src=10.1.0.1, ip_dst=10.1.0.2`; action:
`output=2`. Then the policy variant: same match + priority 100 rule that
`drop`s HTTP (tcp_dst=80) while a lower-priority rule forwards the rest —
priority ordering (the L25 nftables lesson) becomes the lab's scoring rule.

## 7. GA-28: flow-rule exercises (32 min)
Pairs write rules on paper for: (1) H1↔H2 reachability; (2) H2's HTTP blocked,
everything else passes; (3) H1's traffic to H2 mirrored to a monitoring port
(named action; one sentence); (4) after H2 changes IP, predict which rules
break and why (exact-match brittleness — the proactivity debate in miniature).
⚠ Verify rules against a reference controller (or the VM's bridge/nftables
equivalent) before class; handout carries the trace and empty rule table.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "SDN means no hardware" | Same forwarding hardware; the *decision point* moved |
| "The controller makes every packet decision at runtime" | Only the first packet of a flow (reactive); the rest follows installed rules |
| "SDN replaces routing protocols everywhere" | Trade-offs; distributed routing still wins at internet scale (evaluation segment) |
| "OpenFlow = SDN" | OpenFlow is one southbound protocol; the architecture is the idea |
| "Centralized control is a single point of failure by definition" | Replica/partition design exists; the failure is *logical*, mitigated by engineering |

## 9. Suggested practical demonstration
L08's learning-switch demo replayed with a "controller" role: instructor (or a
script) installs bridge rules by hand as packets arrive. ⚠ Pre-script; keep the
GA-28 paper exercise as the protected fallback.

## 10. Classroom activities
- **Plane-sort relay:** 6 behavior cards, teams classify in under 3 minutes.
- **Rules critique:** two pairs read rules aloud; the class finds the priority
  bug before the instructor confirms (peer-teaching, CLO6 evaluation).

## 11. Problem-solving questions
1. Why does reactive installation need a timeout, while proactive doesn't
   necessarily? (stale learning — L08's FDB TTL, again)
2. Your H2-IP-changed rules broke. Propose the controller-side fix (reactive
   re-resolution vs wildcard match).
3. Where does distributed routing still beat SDN? Name one property (scale,
   autonomy, failure isolation).
4. Write a rule pair implementing "H1 can SSH to H2, nobody else can."
5. Why does flow-table priority matter more in SDN than a plain FDB? (overlap +
   policy richness — the L25 ordering lesson)

## 12. Formative assessment (with answers)
- MCQ: "Switch forwards a frame" is a ________ plane action → **data**.
- MCQ: The controller–switch interface is called ________ → **southbound**.
- MCQ: Rules are matched in ________ order → **priority (descending)**.
- Short: one deployment where SDN wins → data-center fabrics / virtual networks
  (accept B4, DC overlays).

## 13. Exit ticket
1. Plane for "policy applied": ________
2. Flow rule = match on ________ + ________.
3. One SDN-vs-distributed trade-off: ________.

## 14. Anticipated difficulties
- Students conflate "centralized" with "single machine"; the consistency
  sentence must be delivered deliberately, not as an aside.
- GA-28's paper format can feel abstract; the trace fields (in_port, IP) ground
  every rule in a packet — do one worked example from the trace before release.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify GA-28 rules against a reference (controller or equivalent); paper exercises printed
- [ ] Board pre-write: planes table; architecture diagram; rule template
- [ ] L08 demo replay scripted; fallback = GA-28 alone

## 16. Timing fallbacks
The architecture segment can lose the OpenFlow naming detail; GA-28's
reachability + policy goals are protected; the mirror exercise may go to
reading. Findings can shrink to one pair if needed.

## 17. References
- PD §4.3 (SDN sections); OpenFlow specification (⚠ verify version/citation
  before assigning); named deployments (Google B4 — verify citation if used).
- L08/L16/L27 notes for continuity; GA-28 handout.
