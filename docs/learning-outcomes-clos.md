# Course Learning Outcomes (CLOs)

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Companion docs | [`course-objectives.md`](course-objectives.md) · [`clo-mapping.md`](clo-mapping.md) · [`assessment-strategy.md`](assessment-strategy.md) |

On successful completion of this course, students will be able to:

---

### CLO1 — Explain the layered architecture (Understand · Bloom C2)
**Explain** the purpose and operation of each layer of the OSI and TCP/IP reference models,
including encapsulation, PDUs, addressing at each layer, and the roles of core protocols and
standards bodies (IEEE 802, IETF/RFCs, ICANN/IANA).

*Evidence:* quizzes, midterm/final exam questions, in-lecture checks.

### CLO2 — Describe physical and data-link operation (Understand/Apply · Bloom C2–C3)
**Describe** how bits actually move: signals and transmission media, framing, error
detection (parity, checksum, CRC), MAC addressing, Ethernet switching behavior (learning,
forwarding, flooding), VLANs, and Wi-Fi operation.

*Evidence:* quizzes, switching/VLAN/Wi-Fi labs and guided activities, exam questions.

### CLO3 — Design addressing plans (Apply/Analyze · Bloom C3–C4)
**Design** IPv4 and IPv6 addressing plans — including subnetting, VLSM, CIDR aggregation,
and NAT boundaries — and **justify** the trade-offs of a given allocation.

*Evidence:* subnetting lab, case study CS-02, midterm exam, capstone design document.

### CLO4 — Analyze real packet flows (Analyze · Bloom C4)
**Capture and analyze** real network traffic with Wireshark/tcpdump to explain the end-to-end
behavior of ARP, ICMP, TCP, UDP, DNS, DHCP, and major application protocols, correctly
attributing observed behavior (retransmissions, timeouts, name-resolution failures) to layer
mechanics.

*Evidence:* packet-analysis labs, case studies CS-01/CS-03/CS-04, exam analysis questions.

### CLO5 — Build and measure networked systems (Apply/Create · Bloom C3–C6)
**Build and instrument** small networked systems using Python sockets and Linux networking
tools; **measure and interpret** performance (throughput, latency, loss, jitter)
quantitatively, including under controlled degradation (`tc netem`).

*Evidence:* UDP-socket lab, TCP performance lab, reliable-transport project (LAB-11),
monitoring lab (LAB-14).

### CLO6 — Evaluate alternatives and troubleshoot systematically (Evaluate · Bloom C5)
**Compare** protocol and design alternatives (e.g., TCP vs UDP, static vs dynamic routing,
wired vs wireless, L2 vs L3 segmentation) and **apply** a structured troubleshooting
methodology to isolate and resolve faults, documenting the process.

*Evidence:* routing labs, case studies, troubleshooting workshop (L29), capstone defense.

### CLO7 — Assess threats and select defenses (Analyze/Evaluate · Bloom C4–C5)
**Assess** common network threats (spoofing, eavesdropping, MITM, DoS/DDoS) and **select**
layered defenses appropriate to a scenario: cryptography and TLS, firewalls and
segmentation, IDS/IPS, VPNs, and monitoring.

*Evidence:* security case study CS-04, firewall lab, exam scenario questions, capstone
security review.

### CLO8 — Integrate in a capstone (Create · Bloom C6)
**Integrate** the above in a team capstone: design, build, secure, instrument, and defend a
small multi-network solution, producing professional documentation, measurement data, and a
defended report.

*Evidence:* capstone deliverables (design doc, working build, monitoring dashboard, final
report, presentation).

---

## Mapping to objectives

| Objective (see [course-objectives.md](course-objectives.md)) | Primarily developed by | Measured by CLOs |
|---|---|---|
| O1 vendor-neutral layered model | Modules 1–2 | CLO1, CLO2 |
| O2 quantitative performance intuition | L01, L18–L20, L28 | CLO4, CLO5, CLO6 |
| O3 packet-analysis literacy | LAB-01 … LAB-14 thread | CLO4 |
| O4 experimentation & programming | Modules 4–5 labs | CLO5 |
| O5 data-science connection | L28, L31, case-study data work | CLO5, CLO6 |
| O6 security & operations thread | L12/L21/L22 previews + Modules 7–8 | CLO7 |
| O7 progressive integration | Case studies CS-01…CS-04, capstone | CLO6, CLO8 |

## PLO mapping — instructor action required
Mapping CLOs to **Program Learning Outcomes (PLOs)** depends on the university's accredited
PLO list, which is not part of this repository. ⚠ VERIFY: the instructor should complete the
PLO mapping table in [`clo-mapping.md`](clo-mapping.md) using their program's official PLO
set before syllabus submission.
