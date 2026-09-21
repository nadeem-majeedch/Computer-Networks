# Case Study Bank — Problem Bank PB-001…PB-065

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS Data Science, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Scope | **65 practice cases (PB-001…PB-065), two per lecture L01–L32 (L29 carries three)** |
| Relationship to the graded thread | Practice only. The graded Meridian cases are **CS-01…CS-04** (25% of course weight, see [`../docs/case-study-strategy.md`](../docs/case-study-strategy.md)); this bank rehearses the same reasoning with **zero direct grade weight** |
| Evidence policy | Synthetic evidence (configs, command output, logs, metric tables) is **clearly labeled synthetic and internally consistent**; no real captures, logs, or measurements are claimed; packet-level evidence is *described*, never fabricated (§4) |
| Files | Each case is one file: student version in the top half, instructor-only version below the horizontal rule — print/extract accordingly |
| Audit | `python3 tools/scripts/audit_casebank.py` (10 checks: inventory, 16-element completeness, split, per-lecture ramp, lecture + task-category coverage, difficulty distribution, index agreement, evidence policy, ID namespace) |

---

## 1. Why this bank exists and how to use it

The graded Meridian thread (CS-01…CS-04) is *longitudinal*: four deep cases stretched across
the semester. What the strategy doc identified as missing — and what this bank supplies — is
**breadth of rehearsal**: 64 short, sharply-focused reasoning cases so students meet every
lecture's core mechanism in *diagnostic* form, not just protocol form.

Typical use (each is optional; nothing here is graded):

- **Opening hooks / closing consolidations** — 5–12 min pair work inside the mapped lecture
  (each case states its designed slot).
- **Tutorial sessions or help-desk hours** — walk in with a case, not a blank page.
- **Exam preparation** — final cases of each lecture pair rehearse exam-style reasoning;
  difficulty and format deliberately mirror the exam's case-vignette questions.
- **Data-science sections** — DS-flagged cases (§5) rehearse transfer math, telemetry
  reasoning, and measurement bias on DS-relevant systems.

## 2. Difficulty model

| Level | Name | What the student must do | Rough share |
|---|---|---|---|
| **Beginner** | Recall → single-step reasoning | One fact, one mechanism, one cause; facts and mechanism both given | 40% (26) |
| **Intermediate** | Guided diagnosis | Multiple facts; 2–3 candidate causes to weigh; simple calculations; one red-herring symptom | 45% (29) |
| **Advanced** | Ambiguous diagnosis | Incomplete or partially conflicting evidence; several plausible causes; student must decide *what to measure next*; multi-step calculations | 11% (7) |
| **Expert** | Design & trade-off | Incomplete requirements; competing constraints; justification and quantitative defense required; "no single right answer" — graded on reasoning quality | 5% (3) |

Progression is enforced per lecture (the second case is never easier than the first) and
across the semester (Module 1–2 cases lean Beginner/Intermediate; later modules carry the
Advanced/Expert share, where students have more layers to reason across).

## 3. Format of each case file

Every case carries the same 16 elements (audit-enforced): unique ID · difficulty · mapped
lecture(s) + CLOs · in-class slot · student scenario · problem statement · evidence pack
(labeled synthetic) · constraints · student questions · expected learning outcomes ·
hints (in the instructor half only) · instructor solution · reasoning process · common
incorrect approaches · extension question · assessment rubric (4-level) · references where
applicable.

Student-facing version = everything above the `---` rule; instructor-only = below it.

## 4. Evidence policy (binding)

1. Every evidence pack begins with the label: **"Synthetic evidence — prepared for this
   case; internally consistent; not from a live system."**
2. Numbers must be *computable*: delays, counts, and sizes follow the arithmetic that the
   solution shows. No case requires believing an impossible number.
3. Packet-level evidence is **described, not fabricated**: a case may say "the capture
   shows …" as *given* evidence, but the bank contains no invented pcap transcripts
   presented as real tool output. Captures that must exist for real are built in the labs
   (LAB-01…16), whose evidence rules are stated there.
4. Facts vs. assumptions: each case marks its **given facts** explicitly; anything the
   student must assume is stated as an assumption in the solution's reasoning.
5. No case requires attacking, probing, or measuring any real external system.

## 5. Data-science integration

Cases with DS-relevant scenarios (19 across the bank: PB-004, PB-006, PB-008, PB-011, PB-019, PB-020, PB-033, PB-034, PB-036, PB-037, PB-038, PB-039, PB-040, PB-053, PB-056, PB-058, PB-061, PB-062, PB-063) rehearse DS-flavored reasoning on networks: transfer-time and overhead math (L03/L04/L31), TCP window/throughput limits for dataset sync (L19/L20), lease/identity churn from managed device fleets (L22), protocol-overhead economics for many-small-file pipelines (L31), and telemetry design/anomaly triage (L29). These map to CLO5 (data-centric networking lens).

## 6. Index — by lecture

| # | Lecture | Cases | Difficulty | Topic category | DS |
|---|---|---|---|---|---|
| 1 | L01 | [PB-001](cases/pb-001-meridian-first-inventory.md), [PB-002](cases/pb-002-rtt-floor-cross-campus.md) | Beginner | Network fundamentals | — |
| 2 | L02 | [PB-003](cases/pb-003-which-layer-failed.md), [PB-004](cases/pb-004-encapsulation-overhead.md) | Beginner | OSI/TCP-IP reasoning | ✓ |
| 3 | L03 | [PB-005](cases/pb-005-sixty-seconds-of-frustration.md), [PB-007](cases/pb-007-three-connections-three-behaviors.md) | Beginner | Network fundamentals · Network programming | — |
| 4 | L04 | [PB-006](cases/pb-006-backup-window-limits.md), [PB-008](cases/pb-008-qos-or-bandwidth.md) | Intermediate | Network performance | ✓ |
| 5 | L05 | [PB-009](cases/pb-009-copper-or-glass-warehouse.md), [PB-010](cases/pb-010-flaky-copper-run.md) | Beginner/Intermediate | Network fundamentals · Physical-layer faults | — |
| 6 | L06 | [PB-011](cases/pb-011-protocol-that-cant-frame.md), [PB-012](cases/pb-012-duplex-mismatch-counters.md) | Beginner/Intermediate | Network programming · Ethernet and switching | ✓ |
| 7 | L07 | [PB-013](cases/pb-013-collision-myth-switched.md), [PB-014](cases/pb-014-pps-vs-bps-firewall.md) | Beginner/Intermediate | Ethernet and switching | — |
| 8 | L08 | [PB-015](cases/pb-015-why-the-reply-went-everywhere.md), [PB-016](cases/pb-016-mac-flapping-mystery.md) | Beginner/Intermediate | Ethernet and switching | — |
| 9 | L09 | [PB-017](cases/pb-017-printer-vanishes.md), [PB-018](cases/pb-018-native-vlan-mismatch.md) | Beginner/Intermediate | VLAN configuration | — |
| 10 | L10 | [PB-019](cases/pb-019-connected-but-slow.md), [PB-020](cases/pb-020-airtime-arithmetic.md) | Beginner/Intermediate | Wireless networking | ✓ |
| 11 | L11 | [PB-021](cases/pb-021-conference-room-dead-zone.md), [PB-022](cases/pb-022-guest-network-design.md) | Intermediate/Expert | Wireless networking · Enterprise network design | — |
| 12 | L12 | [PB-023](cases/pb-023-address-nobody-assigned.md), [PB-024](cases/pb-024-arp-table-forensics.md) | Beginner/Intermediate | IP addressing · ARP and ICMP | — |
| 13 | L13 | [PB-025](cases/pb-025-wrong-subnet-static.md), [PB-026](cases/pb-026-auditing-the-vlsm-plan.md) | Beginner/Intermediate | Subnetting and VLSM | — |
| 14 | L14 | [PB-027](cases/pb-027-two-dhcp-servers.md), [PB-028](cases/pb-028-inside-users-cant-reach-the-published-service.md) | Beginner/Intermediate | DNS/DHCP · NAT | — |
| 15 | L15 | [PB-029](cases/pb-029-link-local-only.md), [PB-030](cases/pb-030-aaa-but-no-path.md) | Beginner/Intermediate | IPv6 | — |
| 16 | L16 | [PB-031](cases/pb-031-longest-prefix-decision.md), [PB-032](cases/pb-032-loop-until-ttl-dies.md) | Beginner/Intermediate | Routing | — |
| 17 | L17 | [PB-033](cases/pb-033-which-process-gets-the-packet.md), [PB-034](cases/pb-034-telemetry-vs-commands.md) | Beginner/Intermediate | Network programming · TCP/UDP behavior | ✓ |
| 18 | L18 | [PB-035](cases/pb-035-half-open-connections.md), [PB-036](cases/pb-036-handshake-ok-transfer-stalls.md) | Beginner/Intermediate | TCP/UDP behavior · Multi-layer troubleshooting | ✓ |
| 19 | L19 | [PB-037](cases/pb-037-reading-the-cwnd-telemetry.md), [PB-038](cases/pb-038-the-buffer-that-ate-the-latency.md) | Intermediate/Advanced | Network performance | ✓ |
| 20 | L20 | [PB-039](cases/pb-039-sizing-your-own-reliability.md), [PB-040](cases/pb-040-design-review-reliable-udp.md) | Intermediate/Advanced | Network programming | ✓ |
| 21 | L21 | [PB-041](cases/pb-041-internal-name-public-answer.md), [PB-042](cases/pb-042-the-migration-that-lagged-behind.md) | Beginner/Intermediate | DNS/DHCP | — |
| 22 | L22 | [PB-043](cases/pb-043-the-805-outage.md), [PB-044](cases/pb-044-the-pool-that-drained-itself.md) | Beginner/Intermediate | DNS/DHCP | — |
| 23 | L23 | [PB-045](cases/pb-045-three-redirects-and-a-cached-lie.md), [PB-046](cases/pb-046-the-api-that-got-slower-on-http2.md) | Beginner/Advanced | Application protocols | — |
| 24 | L24 | [PB-047](cases/pb-047-which-pillar-fell.md), [PB-048](cases/pb-048-the-api-key-that-leaked.md) | Beginner/Intermediate | Security and firewall reasoning | — |
| 25 | L25 | [PB-049](cases/pb-049-the-rule-that-ate-the-subnet.md), [PB-050](cases/pb-050-site-to-site-vpn-blackhole.md) | Intermediate | Security and firewall reasoning | — |
| 26 | L26 | [PB-051](cases/pb-051-the-resolver-that-lied.md), [PB-052](cases/pb-052-hardening-the-shared-lab.md) | Advanced/Expert | Packet capture analysis · Security and firewall reasoning | — |
| 27 | L27 | [PB-053](cases/pb-053-the-port-that-stayed-closed.md), [PB-054](cases/pb-054-container-mtu-mismatch.md) | Beginner/Intermediate | Cloud and data center networking | ✓ |
| 28 | L28 | [PB-055](cases/pb-055-controller-and-the-unknown-unicast.md), [PB-065](cases/pb-065-first-packet-tax.md) | Intermediate | SDN / programmable networks | — |
| 29 | L29 | [PB-056](cases/pb-056-the-destination-that-wasnt-there.md), [PB-057](cases/pb-057-polling-versus-flapping.md), [PB-058](cases/pb-058-the-dashboard-that-lied.md) | Beginner/Intermediate/Advanced | Monitoring and operations | ✓ |
| 30 | L30 | [PB-059](cases/pb-059-married-to-the-wrong-ap.md), [PB-060](cases/pb-060-link-budget-outdoor-bridge.md) | Beginner/Intermediate | Wireless networking | — |
| 31 | L31 | [PB-061](cases/pb-061-many-small-files-many-tears.md), [PB-062](cases/pb-062-campus-upgrade-design-review.md) | Intermediate/Advanced | Data science and distributed computing networks · Enterprise network design | ✓ |
| 32 | L32 | [PB-063](cases/pb-063-the-morning-the-cluster-stopped.md), [PB-064](cases/pb-064-defend-your-capstone.md) | Advanced/Expert | Multi-layer troubleshooting · Enterprise network design | ✓ |

## 7. Index — by difficulty

| Level | Cases | Count |
|---|---|---|
| Beginner | PB-001, PB-002, PB-003, PB-004, PB-005, PB-007, PB-009, PB-011, PB-013, PB-015, PB-017, PB-019, PB-023, PB-025, PB-027, PB-029, PB-031, PB-033, PB-035, PB-041, PB-043, PB-045, PB-047, PB-053, PB-056, PB-059 | 26 |
| Intermediate | PB-006, PB-008, PB-010, PB-012, PB-014, PB-016, PB-018, PB-020, PB-021, PB-024, PB-026, PB-028, PB-030, PB-032, PB-034, PB-036, PB-037, PB-039, PB-042, PB-044, PB-048, PB-049, PB-050, PB-054, PB-055, PB-057, PB-060, PB-061, PB-065 | 29 |
| Advanced | PB-038, PB-040, PB-046, PB-051, PB-058, PB-062, PB-063 | 7 |
| Expert | PB-022, PB-052, PB-064 | 3 |

**Total: 65** — progression: Beginner/Intermediate dominate the early modules; Advanced/Expert concentrate in Modules 4–8 where students have more layers to reason across.

## 8. Index — by topic

| Topic category | Cases |
|---|---|
| ARP and ICMP | PB-024 |
| Application protocols | PB-045, PB-046 |
| Cloud and data center networking | PB-053, PB-054 |
| DNS/DHCP | PB-027, PB-041, PB-042, PB-043, PB-044 |
| Data science and distributed computing networks | PB-061 |
| Enterprise network design | PB-022, PB-062, PB-064 |
| Ethernet and switching | PB-012, PB-013, PB-014, PB-015, PB-016 |
| IP addressing | PB-023 |
| IPv6 | PB-029, PB-030 |
| Monitoring and operations | PB-056, PB-057, PB-058 |
| Multi-layer troubleshooting | PB-036, PB-063 |
| NAT | PB-028 |
| Network fundamentals | PB-001, PB-002, PB-005, PB-009 |
| Network performance | PB-006, PB-008, PB-037, PB-038 |
| Network programming | PB-007, PB-011, PB-033, PB-039, PB-040 |
| OSI/TCP-IP reasoning | PB-003, PB-004 |
| Packet capture analysis | PB-051 |
| Physical-layer faults | PB-010 |
| Routing | PB-031, PB-032 |
| SDN / programmable networks | PB-055, PB-065 |
| Security and firewall reasoning | PB-047, PB-048, PB-049, PB-050, PB-052 |
| Subnetting and VLSM | PB-025, PB-026 |
| TCP/UDP behavior | PB-034, PB-035 |
| VLAN configuration | PB-017, PB-018 |
| Wireless networking | PB-019, PB-020, PB-021, PB-059, PB-060 |

## 9. Instructor adoption checklist

- [ ] Review the two cases for each lecture you teach; swap any that clash with your demo timing
- [ ] Assign 2–3 cases per week as optional tutorial material; never more (protection of lecture time)
- [ ] Keep hints and solutions out of student hands (single-file layout: extract before printing)
- [ ] ⚠ VERIFY arithmetic in calculation cases against your preferred rounding conventions
- [ ] ⚠ VERIFY the ⚠-flagged ⚠ VERIFY items inside individual cases before first use
- ⚠ VERIFY: this checklist item exists to remind you that machine checks cannot confirm pedagogy
- [ ] Map cases onto your own assessment calendar (they are practice; the graded thread is CS-01…04)
