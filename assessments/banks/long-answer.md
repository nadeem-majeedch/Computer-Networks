# Question Bank — Long Answer

| Field | Value |
|---|---|
| Scope | Multi-paragraph reasoning: design justifications, end-to-end narratives, trade-off analyses |
| Marking | Each item carries a **marking outline** (instructor key): points with indicative marks out of 10 |
| Tagging | `[Difficulty|CLO|Source]` |
| Key | fenced at end — do not distribute |

## Questions

**LA-01 [I|CLO1|L01–L03]** Trace one `https://` page load from a dorm PC through every
layer and every device to the server. Name each PDU transformation and each decision
point (ARP, routing, NAT if present).

**LA-02 [I|CLO2|L05–L08]** A 12-story building is wired with one switch per floor and
fiber risers. Justify (i) why floors are separate VLANs, (ii) why risers are trunk
links, (iii) why the router sits at the core, and (iv) one risk the design accepts.

**LA-03 [I|CLO3|L13–L15]** Your /16 campus must serve 40 buildings: 30 need ≤ 500
hosts, 10 are point-to-point-only interconnections. Produce the allocation *logic*
(not every number) and defend where IPv6 would remove a constraint.

**LA-04 [I|CLO4|L18–L20]** Explain what TCP does during: (i) handshake, (ii) steady
bulk transfer, (iii) a loss episode under congestion control. Attribute each behavior
to the mechanism that implements it.

**LA-05 [A|CLO6|L16/L19/L29]** "The transfer was slow" — build the diagnostic tree
from symptom to three distinct root causes (path loss, window limit, RTT-bound), with
the measurement that separates each branch.

**LA-06 [A|CLO7|L24–L26]** Design the security layering for a public web service
reachable from campus and internet: name one control per layer and the attack each
blunts. Justify why no single layer suffices.

**LA-07 [I|CLO5|L17/L20]** A telemetry team wants 10 000 msg/s with loss tolerance
but *ordering* requirements. Argue UDP-with-thin-reliability vs raw TCP: pick one,
justify with the trade-off triangle (latency, reliability, ordering).

**LA-08 [A|CLO6|L21/L22/L29]** Morning outage pattern: DHCP pool exhaustion plus DNS
TTL staleness together. Explain how the two mechanisms interact to *amplify* the
outage's blast radius and duration, and design the two fixes with their trade-offs.

**LA-09 [I|CLO6|L27/L28]** Compare solving "segment tenants safely" with (a) VLANs +
firewalls vs (b) SDN micro-segmentation. Give one workload where each wins and the
operational cost each adds.

**LA-10 [A|CLO6|L29/L30]** A lecture hall's Wi-Fi collapses at class start (200
devices). Diagnose with the airtime/capacity model, then give three mitigations with
their costs, ranked by deployability tonight.

**LA-11 [E|CLO8|L31/L32]** The university wants a data-science teaching cluster in
one building. Produce a design argument covering: addressing, segmentation from
backup traffic, DNS/DHCP services, monitoring, and one capacity calculation you show
openly.

**LA-12 [E|CLO6|L29/L32]** "The dashboard was green." Write the post-incident review
section that explains how green dashboards coexist with brownouts, and name the two
measurement families the revised dashboard must add.

**LA-13 [B|CLO1|L01–L03]** Explain to a non-technical friend why a video call breaks
up when someone else in the house starts a large download. Use the four delay types
in your answer.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE (marking outlines, /10 each)

**LA-01.** Layers correct (DNS→TCP→IP→Ethernet, PDUs named) 3 · ARP/gateway decision 2 ·
NAT/routing hops named 2 · client-side cache/TLS roles 1 · coherent end-to-end order 2.
**LA-02.** (i) per-floor broadcast containment + policy 2 · (ii) trunks carry all VLANs,
tags per 802.1Q 2 · (iii) core = inter-VLAN policy point, one enforcement location 3 ·
(iv) any accepted risk with mechanism (e.g., core = single point; STP dependence; riser
capacity) 3.
**LA-03.** Group buildings into size classes (VLSM by need) 3 · /30-per-link logic 2 ·
growth/alignment rule stated 2 · IPv6: removes scarcity pressure (SLAAC per building,
no NAT chain) with honest note that routing/policy still needs design 3.
**LA-04.** Handshake: ISN sync, options (MSS/window scale), state entry 3 · steady:
min(cwnd,rwnd) pacing, ACK clocking 3 · loss episode: dup-ACK/fast retransmit or RTO,
cwnd reaction (halve/reset) 4.
**LA-05.** Tree has the three named branches 3 · per-branch measurement (loss: retrans
counters/capture; window: rate×RTT implied window vs BDP; RTT-bound: small-file vs
bulk probe) 4 · decision rule stated (which result assigns which cause) 3.
**LA-06.** One control per layer (edge filter, L2 port security, transport TLS,
application authn/authz, monitoring) 4 · attack-to-control mapping 3 · "no single
layer" argument (failure/compromise of one layer leaves others) 3.
**LA-07.** Any defensible pick 2 · trade-off triangle used explicitly (UDP+thin:
sub-RTT timeliness with app-level ordering; TCP: ordering free, head-of-line cost) 5 ·
honest cost named for the pick (retransmit logic, in-order demux buffer) 3.
**LA-08.** Interaction: exhausted pool → APIPA/no-lease clients can't even reach DNS;
stale DNS sends *leased* clients to dead address — failure has two doors, TTL extends
duration after pool fix 4 · fixes: lease-time/pool sizing (trade: churn) + pre-lowered
TTL (trade: query load) 4 · sequencing (lower TTL *before* fixes ship) 2.
**LA-09.** (a) VLAN+firewall: mature, hardware-enforced; wins for stable zoning; cost:
per-change config churn 4 · (b) SDN: per-workload policy (micro-segmentation), wins
for dynamic/multi-tenant workloads; cost: controller dependency + skills 4 · one
explicit workload each 2.
**LA-10.** Model: airtime share = radio goodput ÷ active clients — 200 devices is a
capacity failure, not coverage 3 · mitigations ranked: (1) band-steer to 5 GHz/
more channels (tonight, config-only), (2) add APs/cells (days, hardware), (3) 802.1X/
airtime-fairness tuning (policy) 5 · costs named 2.
**LA-11.** Addressing plan with headroom 2 · backup separation (QoS/VLAN/schedule) 2 ·
services (DHCP scopes, internal DNS) 2 · monitoring (baseline, per-class metrics) 2 ·
capacity calculation shown (e.g., nightly dataset ÷ window → Mb/s; BDP window check) 2.
**LA-12.** Green-vs-brownout mechanism: dashboards summarize *averages* (utilization
fine, p50 latency fine) while tail/p99 RTT and queueing doubled — SLO-blind metrics 4 ·
families to add: latency percentiles (p95/p99) per path; loss/retransmit/queue-depth
counters (and per-class, not device-average) 4 · review section coherent (timeline,
evidence, action) 2.
**LA-13.** /10: uses the taxonomy correctly — download consumes link capacity so the
call's packets *queue* behind it (queueing delay) 3 · serialization spikes on small
frames behind big ones 2 · some packets overflow buffers (loss) → frozen/jumpy video
as the app drops late frames (jitter) 3 · genuinely non-technical prose 2.
