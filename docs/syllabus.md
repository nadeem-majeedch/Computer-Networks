# Course Syllabus — Computer Networks

| Field | Value |
|---|---|
| Course title | Computer Networks |
| Programs | BS Computer Science · BS Data Science |
| Semester | 4th semester |
| Lectures | 32 × 2 hours = 64 instructional hours |
| Lab block | Weekly 2-hour supervised lab (schedule-external; 11 staffed labs) |
| Credit framework | Per university norms (⚠ VERIFY credit-hour equivalence before submission) |
| Prerequisites | See [`prerequisites.md`](prerequisites.md) |
| Status | Draft v0.1 — awaiting instructor review |

> This syllabus is the normative overview. Authoritative detail lives in the companion
> documents: [`schedule-32-lectures.md`](schedule-32-lectures.md),
> [`learning-outcomes-clos.md`](learning-outcomes-clos.md),
> [`clo-mapping.md`](clo-mapping.md), [`assessment-strategy.md`](assessment-strategy.md),
> [`textbooks-references.md`](textbooks-references.md), [`teaching-methodology.md`](teaching-methodology.md),
> [`lab-strategy.md`](lab-strategy.md), [`case-study-strategy.md`](case-study-strategy.md).

---

## 1. Catalog description

A rigorous, vendor-neutral introduction to computer networks for CS and Data Science
undergraduates. Students develop the layered model of networking (OSI/TCP-IP), then study
each layer's mechanisms — from physical media through Ethernet, switching, VLANs, and
Wi-Fi, to IPv4/IPv6 addressing and routing, TCP and UDP, and the core application
protocols. Every major protocol is observed on the wire via packet analysis (Wireshark) and
manipulated in hands-on labs using Python sockets, Linux networking tools, and network
emulation. The course threads security, monitoring, cloud and SDN concepts, mobile
networking, and enterprise design through a progressive case-study narrative, culminating
in a team capstone that designs, builds, secures, instruments, and defends a small
multi-network solution. Data Science students additionally treat network telemetry as data,
covering traffic classification, anomaly-detection framing, and capacity forecasting.

## 2. Course learning outcomes

On successful completion, students will be able to (full text and Bloom levels in
[`learning-outcomes-clos.md`](learning-outcomes-clos.md)):

1. **CLO1** — Explain the layered architecture and core protocols of OSI/TCP-IP networks.
2. **CLO2** — Describe physical- and data-link-layer operation, Ethernet, switching,
   VLANs, and Wi-Fi.
3. **CLO3** — Design IPv4 and IPv6 addressing plans, including subnetting, VLSM, and NAT
   boundaries.
4. **CLO4** — Capture and analyze real packet flows to explain end-to-end protocol
   behavior.
5. **CLO5** — Build and instrument small networked systems and measure their performance
   quantitatively.
6. **CLO6** — Evaluate design alternatives and troubleshoot faults systematically.
7. **CLO7** — Assess common network threats and select layered defenses.
8. **CLO8** — Integrate the above in a team capstone: design, build, secure, instrument,
   and defend a small multi-network solution.

## 3. Weekly lecture calendar

Readings map to [`textbooks-references.md`](textbooks-references.md): **KR** = Kurose &
Ross, *Computer Networking: A Top-Down Approach*; **PD** = Peterson & Davie, *Computer
Networks: A Systems Approach* (free online edition); **T** = Tanenbaum & Wetherall,
*Computer Networks*. Sections are indicative starting points — instructors should verify
against their chosen edition (see the edition-verification note in
[`textbooks-references.md`](textbooks-references.md)).

| Week | Lecture | Topic | Lab / GA | Readings | Assessment due |
|---|---|---|---|---|---|
| 1 | L01 | What is a network? Overview, history & the Internet today | GA-01 Wireshark tour (pre-captured trace) | KR 1.1–1.4; PD 1.1–1.3 | Ethics gate signed (week-1 requirement) |
| 1 | L02 | Layered architectures: OSI & TCP/IP | GA-02 header-dissection puzzle | KR 1.5; PD 1.4–1.5 | — |
| 2 | L03 | Applications, sockets & the first packet hunt | GA-03 socket demo + request journey | KR 2.1, 2.7 | CS-01 in-class exercise |
| 2 | L04 | Performance lab foundations: measuring the network | LAB-01 latency/throughput | KR 1.4 (delay/loss recap) | LAB-01 worksheet |
| 3 | L05 | Physical layer: signals, media, transmission basics | GA-05 Nyquist/Shannon drills | PD 2.1–2.3; T 7.1 | — |
| 3 | L06 | Data link layer: framing, errors & reliability | GA-06 CRC by hand | PD 2.4–2.5 | — |
| 4 | L07 | MAC protocols & wired LANs: Ethernet | GA-07 Ethernet frame dissection | PD 2.6; T 4.3 | — |
| 4 | L08 | Switching & LAN design | GA-08 FDB prediction | PD 3.1–3.2 | **Quiz 1 window opens** (Modules 1–2 to date) |
| 5 | L09 | VLANs & L2 segmentation | LAB-02 switched lab with VLANs | PD 3.2 (VLAN section) | LAB-02 report |
| 5 | L10 | Wireless networking: Wi-Fi fundamentals | LAB-03 Wi-Fi survey + packet analysis | PD 2.7–2.8 | — |
| 6 | L11 | Wireless in practice + LAN security preview | LAB-03 wrap/write-up | KR 6.3 (skim), instructor notes | LAB-03 write-up; **CS-02 kickoff** |
| 6 | L12 | IP fundamentals & ARP | GA-12 ARP resolution walk | KR 4.3.1–4.3.2; PD 3.3 | — |
| 7 | L13 | IPv4 subnetting & VLSM | LAB-04 subnetting drills + design | KR 4.3.3–4.3.4 | — |
| 7 | L14 | IP addressing at scale: DHCP & NAT | LAB-05 DHCP & NAT on Linux router | KR 4.3.4, 4.4.5; PD 3.3.4 | — |
| 8 | L15 | IPv6 | LAB-06 dual-stack lab | KR 4.3.5; PD 4.1 | — |
| 8 | L16 | Routing fundamentals & ICMP | LAB-07 static routing + traceroute dissection | KR 4.3, 5.1–5.2 (intro); PD 3.3.2 | LAB-04 problem set due; **MIDTERM** (in lecture) |
| 9 | L17 | UDP & the transport layer's job | LAB-08 UDP chat/file transfer (Python) | KR 3.1–3.3 | LAB-05/06/07 reports |
| 9 | L18 | TCP essentials: connections & reliable delivery | GA-18 handshake & retransmission dissection | KR 3.5.1–3.5.4 | LAB-08 demo |
| 10 | L19 | TCP flow & congestion control | LAB-09 TCP performance with netem | KR 3.5.5, 3.6–3.7 | — |
| 10 | L20 | Programming the transport layer: reliability over UDP | Assign LAB-10/11 reliable-transport project | KR 3.4; instructor project notes | **Project spec due** (graded milestone) |
| 11 | L21 | DNS: the Internet's directory | GA-21 dig drills + resolution capture | KR 2.4; PD 9.3.1 | — |
| 11 | L22 | DHCP deep dive, BOOTP & address management | GA-22 DORA dissection + IPAM exercise | KR 4.4.5 (revisit); RFC 2131 skim | — |
| 12 | L23 | Core application protocols: HTTP/1.1 → HTTP/3, SMTP, SSH | LAB-12 protocol comparison captures | KR 2.2–2.3, 2.5 | **CS-03 kickoff**; LAB-09 report |
| 12 | L24 | Security principles & cryptographic building blocks | GA-24 certificate chain + TLS worksheet | KR 8.1–8.3, 8.5 | **Quiz 2 window opens** (Modules 4–5 + project) |
| 13 | L25 | Perimeter & internal defenses: firewalls, segmentation, VPNs | LAB-13 firewalls & VPN lab | KR 8.4–8.9 (selected); PD 8.3 | — |
| 13 | L26 | Attack & defense case workshop | GA-26 benign SYN-flood emulation + defense | Instructor notes (RFC 2131, BCP 38 concept) | **CS-03 diagnosis due**; **Group project report due** (capstone stage 2 + CS-04 brief) |
| 14 | L27 | Cloud & virtual networking | GA-27 mini-VPC build | PD 3.4, 4.3 (selected); instructor cloud notes | — |
| 14 | L28 | Data-plane & SDN: programmable networks | GA-28 SDN/telemetry demo + flow-record analysis | PD 3.5 (SDN section) | — |
| 15 | L29 | Monitoring, telemetry & systematic troubleshooting | LAB-14 monitoring dashboard + fault drill | PD 8.1–8.2; instructor notes | **LAB-14 report; CS-03 RCA report due** |
| 15 | L30 | Mobile & wireless enterprise networking | GA-30 campus wireless design worksheet | KR 6.3–6.4 (skim); PD 2.7 | — |
| 16 | L31 | Enterprise design & the data-science connection | GA-31 full-network design review (peer critique) | KR 5.7 (skim); instructor design notes | Peer-review sheet; CS-04 design brief |
| 16 | L32 | Capstone workshop, presentations & course synthesis | Capstone build + present | Course synthesis notes | **Capstone deliverables due; presentations** |

> ⚠ VERIFY: weeks 8 and 16 assume the standard 16-week semester with a finals week. Adjust
> the midterm and capstone defense dates to your academic calendar before publication.

## 4. Assessment summary

Weights and instruments are defined in
[`assessment-strategy.md`](assessment-strategy.md). Summary:

| Instrument | Weight |
|---|---|
| Quizzes (2 best of 4) | 10% |
| Labs & guided activities | 15% |
| Subnetting problem set | 5% |
| Midterm examination | 20% |
| Reliable-transport project | 10% |
| Case studies CS-01–CS-03 | 10% |
| Capstone (all deliverables) | 15% |
| Final examination | 15% |
| **Total** | **100%** |

## 5. Course policies (summary)

- **Attendance:** lab attendance is required for group work; lecture attendance strongly
  recommended (GA submissions are collected in lecture). ⚠ VERIFY against university policy.
- **Late work:** labs/projects — 10% per 24 h up to 48 h, then 0; capstone milestones — no
  late window (dependency chain). ⚠ VERIFY final late policy with program rules.
- **Academic integrity:** collaboration rules differ by instrument — labs and the capstone
  are collaborative; quizzes and exams are strictly individual; case-study write-ups are
  individual even when analysis is discussed. All code and packet evidence must be
  reproducible on demand. Generative-AI use follows university policy — ⚠ VERIFY.
- **Ethics gate:** the week-1 acknowledgment in [`prerequisites.md`](prerequisites.md) is
  mandatory before participating in Labs 03, 08–14 and GA-26.

## 6. Instructor adaptation notes

- The syllabus is coherent as written; if your semester has fewer than 16 teaching weeks,
  compress by moving enrichment (enr) topics out, then merge L21+L22 or L27+L28 — do not
  remove L13 (subnetting), L18–L19 (TCP), or L24 (security foundations).
- Data Science section emphasis: expand L28 and L31 data-science segments into a full
  activity; CS/DS can share all other content unchanged.
