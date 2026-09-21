# LAB-15 — Instructor Guide

## Setup / duty of care (before session)
- Ship three scaffolds: sequential connect-scan pattern (Python, ~20 lines), plain HTTP
  victim server, 4-line gratuitous-ARP spoofer. Slow-by-design tools keep the shape visible
  and make rate-based detection natural.
- **Verify each pair's topology before T3** (README duty): three namespaces + bridge,
  nothing bridged outward. The lab's safety argument depends on this check.
- Generate the offline captures from your own run; redact nothing (all synthetic).

## Solutions / expected values
- **Pre-lab 1:** SYN (no payload/ACK); open → SYN/ACK, closed → RST, filtered → silence.
- **Pre-lab 2:** gratuitous ARP reply; victim caches IP→(wrong) MAC.
- **Pre-lab 3:** TLS protects confidentiality/integrity of the session; MITM degrades to
  metadata + failed cert validation.
- **T2:** footprint = N SYNs / T seconds to distinct ports, zero payload; NAT false
  positive is the expected answer.
- **T3:** before/after neighbor-table evidence is the deliverable; the "defense already on"
  troubleshooting row is a teaching gift — use it aloud.
- **T4:** SNI, IPs, sizes, timing remain; cert validation failure is the visible defeat of
  active MITM.
- **T5:** thresholds trade sensitivity vs FPR; the normal capture gives the FPR number —
  require both numbers (TP and FP), not vibes.

## Common failure modes
1. Pairs improvising with external attack tooling "to be realistic" — stop it at the gate;
  the scaffolds exist precisely so the *shape* is visible without the tooling.
2. Skipping the false-positive half of T5 — half the defender's job is not crying wolf.
3. Reports glorifying attack mechanics over detection — grading weights the defender's side.

## Recognition grading (no course weight)
Recognition = demo + one-page findings: detection rules with TP/FP numbers, the T4 TLS
argument, and the economics table. Exceptional pairs present 5 minutes in L26's workshop
slot if time allows (instructor's call).
