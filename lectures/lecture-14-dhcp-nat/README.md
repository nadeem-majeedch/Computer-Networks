# Lecture 14 — IP Addressing at Scale: DHCP & NAT

| Field | Value |
|---|---|
| Module | 3 — Internetworking with IPv4/IPv6 |
| Depends on | L12 (IP model), L13 (subnetting/notation) |
| CLOs addressed | **CLO3** (primary), CLO4 (packet analysis) |
| Bloom level | C3 |
| Assessment artifact | Lab report (LAB-05) |
| Lab | LAB-05: configure DHCP & NAT on a Linux router (VM lab, pairs) |
| Readings | KR §4.3.4 (DHCP), §4.4.5 (NAT, ⚠ verify); RFC 2131 (skim); RFC 3022 (skim) |
| Prerequisites | L12–L13; LAB-04 submitted |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-05 handout (labs/) |

## Key questions
- How does a device join a network and get an address without any manual configuration?
- How do thousands of private addresses share one public IP — and what breaks?
- What is NAT actually doing to packets, field by field?

## What you should be able to do afterwards
- Walk the DHCP DORA exchange and the lease lifecycle (renewal, rebinding, expiry).
- Configure DHCP and NAT on a Linux router and verify each on the wire.
- Explain NAT's address/port rewriting mechanics and its consequences for apps.
- Place public/private addressing and registries (IANA/RIRs) in the allocation story.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-05 handout

## Homework / preparation for next lecture
- LAB-05 report due. Read KR §4.3.5 (IPv6) — bring one question about "why a new IP".
