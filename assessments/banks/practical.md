# Question Bank — Practical Assessment

| Field | Value |
|---|---|
| Scope | Hands-on checks: build, measure, capture, diagnose on the course lab stack |
| Environment rule | Every item runs **inside the course's isolated lab environment** (namespaces/VMs/offline captures) per [`../../labs/syllabus-safety.md`](../../labs/syllabus-safety.md) — never against external systems |
| Tagging | `[Difficulty|CLO|Source]`; pairs with the LAB rubric in [`../rubrics/practical-work-rubric.md`](../rubrics/practical-work-rubric.md) |
| Key | fenced at end — do not distribute |
| Honesty note | Expected observations derive from tool semantics; instructors run the task once before grading (ITI rule) |

## Tasks

**PR-01 [B|CLO5|LAB-01]** Measure RTT to your lab gateway: run 20 pings, report min/avg/
max, and state whether max−min spread is within one baseline-jitter judgment.

**PR-02 [I|CLO5|LAB-01]** Two `iperf3` runs: default window vs `-w 512k`. Predict
which is higher on a 30 ms RTT loopback-netem path and verify; explain via BDP.

**PR-03 [I|CLO5|LAB-02]** Build two namespaces bridged on `br0` with `vlan_filtering=1`;
prove h1 (VLAN 10) cannot reach h2 (VLAN 20) while ping between same-VLAN hosts works.
Submit commands + two ping outputs.

**PR-04 [I|CLO4|LAB-02]** Capture 20 s on the trunk while both VLANs ping: show one
tagged and one untagged frame from the capture, naming the 802.1Q field values.

**PR-05 [I|CLO4|LAB-05]** In the DNS/DHCP namespace lab, capture the DORA exchange:
label all four packets with their broadcast/unicast nature as observed.

**PR-06 [I|CLO4|LAB-08]** Write a 10-line UDP echo client/server; run them in two
namespaces; capture the datagrams and annotate ports both ways.

**PR-07 [A|CLO5|LAB-09]** On the netem path (50 ms each direction), produce `iperf3`
results for: base, +1% loss, +2% loss. Report the throughput drop pattern and explain
it via RTO/window behavior.

**PR-08 [I|CLO4|LAB-06]** Show your namespace has: (i) an fe80:: address, (ii) the
IPv4 default route. Explain which one DAD applies to.

**PR-09 [I|CLO6|LAB-07]** Given the two-router topology with one deliberately wrong
static route (set by the instructor), find it with `ip route` + `traceroute` evidence
and state the exact corrected line.

**PR-10 [I|CLO7|LAB-13]** Implement the two nftables rules from the brief (allow
established/related; drop new inbound on the protected port); demonstrate one allowed
and one blocked flow with evidence.

**PR-11 [A|CLO6|LAB-14]** The lab's fault-injection helper breaks one thing in your
topology (unknown to you). Diagnose within 15 minutes using only allowed commands;
submit an ordered evidence log.

**PR-12 [I|CLO4|LAB-12]** From the offline HTTP trace: identify HTTP/1.1 vs HTTP/2
frames, count parallel streams on the H2 connection, and state what would have
stalled under HTTP/1.1.

**PR-13 [E|CLO6|LAB-11/14]** Run your reliable-transport project against the loss
profile (1%, 2%); submit throughput numbers and a one-paragraph interpretation
naming the limiting mechanism (RTO policy vs window).

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**PR-01.** Accept any real 20-probe run; judgment line must compare spread against the
session's own variability (not "0 ms = good"). **PR-02.** Default (small window)
should lose: 30 ms BDP ≈ 3.75 MB ≫ small window — verified by the student's own runs;
explanation ties measured rate ≈ window/RTT. **PR-03.** Success: same-VLAN pings work;
cross-VLAN pings fail *at L2* (no ARP reply) — commands reproducible; the common
failure (filtering left on, wrong vlan id on the port) is a troubleshooting finding,
not a lost cause. **PR-04.** Tagged frame shows vlan id 10 or 20 (TPID 0x8100);
untagged appears on access-side captures. Both named fields earn the mark. **PR-05.**
Discover: broadcast; Offer: typically unicast (observe!); Request: broadcast (or
unicast renew); Ack: typically unicast. *Observed* labels, not memorized ones, earn
the mark — course honesty rule. **PR-06.** Working echo loop + capture showing client
ephemeral port ↔ server 7005 (or the brief's port); annotation names both directions.
**PR-07.** Pattern: throughput falls sharply as loss rises (RTO stalls + window
collapse); exact numbers vary by kernel/build — students report *their* numbers and
the pattern, not a canonical figure. **PR-08.** fe80:: present via SLAAC; IPv4
default route via config/DHCP. DAD applies to the SLAAC-assigned global/link-local
IPv6 address (ARP/ND-probe before use), not to the manually configured v4 route.
**PR-09.** Evidence: `traceroute` diverges at the wrong router; `ip route` shows the
offending prefix. Corrected line must match the topology's true next hop. **PR-10.**
Allowed flow passes (established/related match), new inbound to protected port drops
(policy match); evidence = command outputs or counters, not claims. **PR-11.**
Graded on *method*: ordered hypotheses (L2 → L3 → services), each with the command
run and result; identifying the injected fault earns the outcome mark. **PR-12.**
H1.1: request/response pairs, head-of-line serialization; H2: one TCP connection,
stream identifiers interleaved. Stall answer: all streams would serialize behind one
outstanding request/response pair. **PR-13.** Numbers vary by implementation — graded
on measurement honesty (exact commands, no rounding-to-hoped-for) and interpretation
naming *their* limiter from the two candidates with evidence.
