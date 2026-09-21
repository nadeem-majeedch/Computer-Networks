# CLO-to-Topic and CLO-to-Assessment Mapping

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Companions | [`learning-outcomes-clos.md`](learning-outcomes-clos.md) · [`schedule-32-lectures.md`](schedule-32-lectures.md) · [`assessment-strategy.md`](assessment-strategy.md) |

This document answers two questions: **where is each CLO taught?** (topics + lectures) and
**where is each CLO measured?** (assessment instruments). It is the primary coherence check
used by the foundation audit.

---

## 1. CLO-to-topic matrix

Legend: **●** primary coverage (taught and practiced in depth) · **◐** supporting coverage
(revisited or applied) · **○** context only.

| Lecture | Topic cluster | CLO1 | CLO2 | CLO3 | CLO4 | CLO5 | CLO6 | CLO7 | CLO8 |
|---|---|---|---|---|---|---|---|---|---|
| L01 | Network overview, history, delay/loss taxonomy | ● | ○ | | ◐ | ◐ | | | |
| L02 | OSI & TCP/IP layering, encapsulation, standards | ● | ◐ | | | | | | |
| L03 | Applications, sockets, end-to-end path | ● | | | ◐ | ◐ | | | |
| L04 | Performance measurement foundations (LAB-01) | | | | ● | ● | ◐ | | |
| L05 | Physical layer: signals, media, capacity | ◐ | ● | | | | | | |
| L06 | Data link: framing, errors, CRC | | ● | | | | | | |
| L07 | MAC protocols & Ethernet | ◐ | ● | | ◐ | | | | |
| L08 | Switching & LAN design | | ● | | ◐ | | ◐ | | |
| L09 | VLANs & L2 segmentation (LAB-02) | | ● | ◐ | | | ● | ◐ | |
| L10 | Wi-Fi fundamentals (LAB-03) | | ● | | ◐ | | ◐ | | |
| L11 | Wireless practice + LAN security preview | | ● | | ◐ | | ● | ◐ | |
| L12 | IP fundamentals & ARP (GA-12) | ◐ | ● | ◐ | ● | | | ◐ | |
| L13 | Subnetting & VLSM (LAB-04) | | | ● | | | ◐ | | |
| L14 | DHCP & NAT (LAB-05) | | | ● | ◐ | | | | |
| L15 | IPv6 (LAB-06) | | | ● | ◐ | | | | |
| L16 | Routing fundamentals & ICMP (LAB-07) | | | ● | ● | | ● | | |
| L17 | UDP & sockets (LAB-08) | | | | ◐ | ● | ◐ | | |
| L18 | TCP connections & reliability (GA-18) | | | | ● | ◐ | | | |
| L19 | TCP flow & congestion control (LAB-09) | | | | ● | ● | ◐ | | |
| L20 | Reliable transport over UDP (LAB-10/11 project) | | | | ◐ | ● | ● | | |
| L21 | DNS (GA-21) | | | | ● | | | ◐ | |
| L22 | DHCP deep dive & address management (GA-22) | | | ◐ | ● | | | ◐ | |
| L23 | HTTP/2/3, SMTP, SSH (LAB-12) | | | | ● | ◐ | ◐ | | |
| L24 | Security principles, crypto, TLS (GA-24) | | | | ◐ | | | ● | |
| L25 | Firewalls, segmentation, VPNs (LAB-13) | | | ◐ | | | | ● | |
| L26 | Attack & defense case workshop | | | | ● | | ◐ | ● | |
| L27 | Cloud & virtual networking (GA-27) | | | ◐ | | | ● | ◐ | |
| L28 | SDN & programmable networks (GA-28) | ◐ | | | | | ● | | |
| L29 | Monitoring & troubleshooting (LAB-14) | | | | ● | ● | ● | ◐ | |
| L30 | Mobile & wireless enterprise networking | | ◐ | | | | ● | | |
| L31 | Enterprise design & data-science connection | | | ◐ | | | ● | ◐ | ◐ |
| L32 | Capstone workshop & synthesis | | | ◐ | ◐ | ◐ | ● | ◐ | ● |

### CLO coverage summary

| CLO | Primary lectures | Supporting lectures | Verdict |
|---|---|---|---|
| CLO1 Layered architecture | L01, L02, L03 | L05, L07, L12, L28 | Covered |
| CLO2 Physical & data link | L05–L12, L30 | L02, L07 | Covered |
| CLO3 Addressing design | L13, L14, L15, L16 | L09, L25, L27, L31, L32 | Covered |
| CLO4 Packet analysis | L04, L12, L16, L18, L21, L22, L23, L26, L29 | L03, L07–L11, L17, L19 | Covered |
| CLO5 Build & measure | L04, L17, L19, L20, L29 | L01, L03 | Covered |
| CLO6 Evaluate & troubleshoot | L09, L11, L16, L20, L26–L29, L30, L31, L32 | L04, L08, L23 | Covered |
| CLO7 Threats & defenses | L24, L25, L26 | L09, L11, L12, L21, L22, L27, L29, L31 | Covered |
| CLO8 Capstone integration | L31, L32 | L13, L16, L26, L29 | Covered |

Enrichment topics are excluded from the coverage verdicts above; every CLO is satisfied by
**core** content alone.

## 2. CLO-to-assessment matrix

Instruments are defined in [`assessment-strategy.md`](assessment-strategy.md).
**ITI** = instructor-verified tool check required before first use (see
[`contributing-instructor-review.md`](contributing-instructor-review.md)).

| Instrument | Type | CLO1 | CLO2 | CLO3 | CLO4 | CLO5 | CLO6 | CLO7 | CLO8 | Weight |
|---|---|---|---|---|---|---|---|---|---|---|
| Quizzes (2 best of 4) | Individual | ✔ | ✔ | ✔ | ✔ | | | ◐ | | 10% |
| Labs & guided activities | Individual | ◐ | ✔ | ✔ | ✔ | ✔ | ◐ | ◐ | | 15% |
| Subnetting problem set | Individual | | | ✔ | | | | | | 5% |
| Midterm examination | Individual | ✔ | ✔ | ✔ | ✔ | | ◐ | | | 20% |
| Reliable-transport project (LAB-10/11) | Pair | | | | ✔ | ✔ | ✔ | | | 10% |
| Case studies CS-01–CS-03 | Individual | | ◐ | ✔ | ✔ | ◐ | ✔ | ✔ | | 10% |
| Capstone (all deliverables) | Team | | ◐ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | 15% |
| Final examination | Individual | ✔ | ✔ | ✔ | ✔ | ◐ | ✔ | ✔ | | 15% |
| **Total** | | | | | | | | | | **100%** |

### CLO measurement coverage check

| CLO | Measured by | Coverage verdict |
|---|---|---|
| CLO1 | Quizzes, midterm, final, labs | ✔ ≥2 instruments |
| CLO2 | Quizzes, labs, midterm, final, case studies | ✔ ≥2 instruments |
| CLO3 | Quizzes, subnetting problem set, labs, midterm, case studies, capstone, final | ✔ ≥2 instruments |
| CLO4 | Quizzes, labs, midterm, reliable-transport project, case studies, capstone, final | ✔ ≥2 instruments |
| CLO5 | Labs, reliable-transport project, final, capstone | ✔ ≥2 instruments |
| CLO6 | Labs, reliable-transport project, case studies, capstone, final | ✔ ≥2 instruments |
| CLO7 | Quizzes, labs, case studies, capstone, final | ✔ ≥2 instruments |
| CLO8 | Capstone only | ✔ 1 instrument by design (see note) |

> **Note on CLO8:** capstone integration is inherently measured by the capstone. The final
> examination's synthesis question and the L31 peer-review sheet provide corroborating but
> non-counting evidence. ⚠ VERIFY: if your quality-enhancement cell requires ≥2 graded
> instruments per CLO, add a small capstone stage-gate rubric (e.g., design-document review)
> as a separately recorded item within the capstone weight.

## 3. Bloom-level progression check

- Module 1–2 (L01–L11): predominantly C1–C3 — build vocabulary and mechanics.
- Module 3–5 (L12–L23): predominantly C3–C4 — design and analyze.
- Module 6–8 (L24–L32): predominantly C4–C6 — evaluate, defend, create.

No module regresses below its predecessor's floor, satisfying the "foundational before
advanced" requirement.

## 4. PLO mapping — instructor action required

⚠ VERIFY: the table below is intentionally left incomplete. Map each CLO to your
university's official Program Learning Outcomes before syllabus submission; do not guess.

| CLO | PLO code | PLO statement | Mapping strength |
|---|---|---|---|
| CLO1 | _pending_ | _from accredited PLO list_ | _pending_ |
| CLO2 | _pending_ | _pending_ | _pending_ |
| CLO3 | _pending_ | _pending_ | _pending_ |
| CLO4 | _pending_ | _pending_ | _pending_ |
| CLO5 | _pending_ | _pending_ | _pending_ |
| CLO6 | _pending_ | _pending_ | _pending_ |
| CLO7 | _pending_ | _pending_ | _pending_ |
| CLO8 | _pending_ | _pending_ | _pending_ |
