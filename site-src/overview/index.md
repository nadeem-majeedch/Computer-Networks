---
title: Course Overview
icon: material/book-open-variant
---

# Course Overview

This page condenses the course's foundation documents; each links to the full
version used by instructors.

## Description

A complete undergraduate Computer Networks course: **32 lectures × 2 hours
(64 instructional hours)** combining theory, packet analysis, Python/Linux
laboratories, network emulation, progressive case studies, and a capstone.
The course explains foundational concepts before advanced ones, separates core
topics from enrichment, and never reduces to vendor certification.

- **Audience**: 4th-semester BS Computer Science and BS Data Science students
- **Contact hours**: 64 lecture hours + a weekly 2-hour supervised lab block
- **Full syllabus**: [docs/syllabus.md](../docs/syllabus.md) *(course-source copy)*

## Prerequisites

| Prior course | Level | Why it matters |
|---|---|---|
| Programming Fundamentals (CS1) | **Required** | Labs are in Python; socket programming in Module 4 |
| Computer Organization / Architecture | **Required** | How machines, buses, and bits behave |
| Discrete Mathematics | **Required** | Powers of two, modular arithmetic (CRC, subnetting) |
| Operating Systems (concurrent) | Recommended | Processes, permissions, virtualization |
| Linear Algebra / Statistics | Helpful (DS track) | Measurement and monitoring topics |
| Data Structures | Helpful | Building a reliable-transport protocol (Module 4 project) |

Details and the entry-skills self-check: [docs/prerequisites.md](../docs/prerequisites.md).

## Course Learning Outcomes (CLOs)

| CLO | Outcome |
|---|---|
| **CLO1** | Explain network architecture, layering, and encapsulation |
| **CLO2** | Explain physical- and data-link operation; reason about media trade-offs |
| **CLO3** | Design IPv4/IPv6 addressing and subnet plans |
| **CLO4** | Capture, dissect, and interpret packets and protocol behavior |
| **CLO5** | Build and measure small networks and transport endpoints |
| **CLO6** | Diagnose, evaluate, and troubleshoot networks and designs |
| **CLO7** | Analyze threats and select layered defenses |
| **CLO8** | Integrate all of the above in a full design lifecycle (capstone) |

Full mapping of CLOs to topics, lectures, and assessments:
[docs/clo-mapping.md](../docs/clo-mapping.md) and
[assessments/clo-assessment-mapping.md](../assessments/clo-assessment-mapping.md).

## Topic progression

The semester runs through eight modules — every module's floor is at or above its
predecessor's Bloom level:

1. **Foundations** (L01–L04) — what networks are; delay/loss; layering; measurement
2. **Physical & Data Link** (L05–L11) — signals, framing, Ethernet, switching, VLANs, Wi-Fi
3. **Internetworking** (L12–L16) — IP, ARP, subnetting/VLSM, DHCP/NAT, IPv6, routing
4. **Transport** (L17–L20) — UDP, TCP, flow/congestion control, a reliable-transport project
5. **Applications** (L21–L23) — DNS, DHCP deep dive, HTTP/2·3, SMTP, SSH
6. **Network Security** (L24–L26) — crypto/TLS, firewalls/VPNs, attack–defense workshop
7. **Operations, Cloud & SDN** (L27–L29) — virtual/cloud networking, SDN, monitoring
8. **Integration & Capstone** (L30–L32) — mobile/enterprise wireless, design, capstone

Per-lecture detail: [the lecture index](../lectures/README.md) and
[docs/schedule-32-lectures.md](../docs/schedule-32-lectures.md).

## Assessment strategy

| Instrument | Weight (proposed plan) |
|---|---|
| Quizzes (best 2 of 4) | 10% |
| Labs & guided activities (13 deliverables, drop lowest) | 15% |
| Subnetting problem set | 5% |
| Midterm examination (W8) | 20% |
| Reliable-transport project | 10% |
| Case studies CS-01–CS-03 | 10% |
| Capstone (all deliverables) | 15% |
| Final examination (cumulative) | 15% |

!!! note "Proposed weighting"

    All weights are the **proposed plan** in
    [docs/assessment-strategy.md](../docs/assessment-strategy.md) §2 — internally
    consistent and summing to 100%, but subject to the institution's confirmed
    policy. Rubrics award instrument-local marks (e.g., midterm /60) so any final
    weighting survives.

Student-facing papers, banks, and rubrics:
[the assessments area](../assessments/README.md).

## Learning expectations

- **Evidence discipline**: any claimed measurement or capture must be reproducible
  from submitted commands, filters, and files; fabricated evidence scores zero on
  the whole instrument.
- **Ethics gate**: a week-1 acknowledgment governs all capture and attack-emulation
  work — isolated lab environments only, no probing of external systems.
- **Explainability**: every member of a pair/team must be able to explain any
  submitted part on demand.
- **Integrity & AI use**: see
  [assessments/academic-integrity.md](../assessments/academic-integrity.md)
  (⚠ institution's current policy overrides the course default).

## Recommended references

Primary texts and standards are listed on the [References](../references.md)
page with full attribution.
