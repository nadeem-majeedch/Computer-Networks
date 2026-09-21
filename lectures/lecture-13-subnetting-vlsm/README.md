# Lecture 13 — IPv4 Subnetting & VLSM

| Field | Value |
|---|---|
| Module | 3 — Internetworking with IPv4/IPv6 |
| Depends on | L12 (addresses, notation) |
| CLOs addressed | **CLO3** (primary) |
| Bloom level | C3–C4 |
| Assessment artifact | Graded subnetting problem set (LAB-04, due L16) |
| Lab | LAB-04: subnetting drills + design exercise (starts; due L16) |
| Readings | KR §4.3.3–4.3.4; PD §3.3 (addressing) |
| Prerequisites | L12; binary/dotted-decimal fluency (prep drill assigned) |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-04 handout (labs/) |

## Key questions
- Given any address/prefix, how do you instantly find the network, broadcast, and host
  range?
- How do you slice one allocation into differently-sized subnets with no waste (VLSM)?
- Why does route aggregation shrink the global routing table?

## What you should be able to do afterwards
- Compute network/broadcast/host ranges for any prefix mentally for /24-class cases.
- Design a VLSM plan for a multi-size requirements table.
- Aggregate contiguous prefixes into shorter ones.
- Justify growth headroom and documentation choices in a plan.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-04 handout

## Homework / preparation for next lecture
- LAB-04 design exercise (bring questions to L14). Read KR §4.3.4, §4.4.5 (DHCP/NAT).
