# Course Learning Objectives

| Field | Value |
|---|---|
| Course | Computer Networks (BS Computer Science / BS Data Science, Semester 4) |
| Scope | 32 lectures · 2 hours each · 64 instructional hours |
| Status | Draft v0.1 — awaiting instructor review |
| Reviewed by | _pending_ |

Course **objectives** state what the course is designed to do instructionally. They are
instructor-facing intents. The measurable, student-facing commitments derived from them are
the **Course Learning Outcomes (CLOs)** in
[`learning-outcomes-clos.md`](learning-outcomes-clos.md).

---

## Objectives

**O1 — Build a rigorous, vendor-neutral model of networking.**
Establish the layered architecture of computer networks (OSI and TCP/IP) as the primary
mental model, grounded in open standards (IEEE 802, IETF RFCs) rather than any vendor's
product taxonomy. The course is explicitly **not** a certification-preparation course.

**O2 — Develop quantitative intuition for network performance.**
Teach students to reason with numbers: bandwidth vs throughput, propagation vs
transmission delay, bandwidth–delay product, loss and retransmission cost, and how queues
create latency. Students should be able to *estimate* before they *measure*.

**O3 — Build packet-analysis literacy.**
Make packet capture and analysis (Wireshark, tcpdump) a reflex: every major protocol is
observed on the wire, not only described. Students should be able to explain ARP, ICMP,
TCP, UDP, DNS, DHCP, and HTTP behavior from real traces.

**O4 — Develop experimentation and programming skills for networking.**
Use Python sockets, Linux networking tools (`ip`, `ss`, `tc`, network namespaces), and
emulation (`netem`) so students can build small networked systems, perturb them, and
interpret the results — including writing a reliable transport protocol over UDP.

**O5 — Connect networking to data-science practice.**
For the BS Data Science audience: treat network telemetry (flow records, captures, device
metrics) as data. Introduce traffic classification, anomaly detection framing, measurement
bias, and capacity forecasting as applied data problems, without turning the course into a
machine-learning course.

**O6 — Thread security and operations through the whole course, then consolidate.**
Introduce threats where they first become visible(ARP spoofing in L12, DNS poisoning in L21, DHCP starvation in L22), then consolidate with a dedicated security module, a
monitoring/troubleshooting module, and an operations-oriented case-study thread.

**O7 — Integrate everything in a progressive, authentic context.**
Run one fictional organization ("Meridian Systems") through four escalating case studies
and a team capstone (design → build → secure → instrument → defend → present), so concepts
are repeatedly applied in an enterprise-design context rather than memorized in isolation.

---

## Positioning constraints (deliberate design decisions)

1. **Fourth-semester level.** Foundational before advanced; no graduate-level digressions.
   Depth is signaled per lecture in the [master schedule](schedule-32-lectures.md).
2. **Required vs enrichment separation.** Each lecture's schedule row labels core topics
   and `(enr)` enrichment topics. Enrichment may be skipped without breaking coherence.
3. **Spiral, not siloed.** Some topics intentionally appear twice at increasing depth
   (e.g., TLS usage in L24, TLS mechanism in L26;UDP as transport in L17, UDP as QUIC substrate in L23). This is planned spiraling, not redundancy.
4. **Realism.** Only tools and labs that run on commodity laptops, VMs, or free cloud tiers
   are required. Anything environment-dependent is marked for instructor verification
   (see [`lab-strategy.md`](lab-strategy.md) and
   [`contributing-instructor-review.md`](contributing-instructor-review.md)).
