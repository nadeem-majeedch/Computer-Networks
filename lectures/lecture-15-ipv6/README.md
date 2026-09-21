# Lecture 15 — IPv6

| Field | Value |
|---|---|
| Module | 3 — Internetworking with IPv4/IPv6 |
| Depends on | L12 (IPv4 model), L13 (subnetting), L14 (DHCP/NAT) |
| CLOs addressed | **CLO3** (primary), CLO4 (dual-stack packet analysis) |
| Bloom level | C3 |
| Assessment artifact | Lab report (LAB-06) |
| Lab | LAB-06: dual-stack IPv4+IPv6 lab (VMs, capture both) |
| Readings | KR §4.3.5; RFC 8200 (skim); PD §4.1 (perspective) |
| Prerequisites | L12–L14 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-06 handout (labs/) |

## Key questions
- Why did IPv4 run out, and how do 340 undecillion addresses change the design?
- How do IPv6 addresses work — structure, types, abbreviation rules?
- How does a host get its addresses *without* DHCP (and when does it still use one)?

## What you should be able to do afterwards
- Read, abbreviate, and plan IPv6 addresses (GUA, LLA, ULA, multicast).
- Explain SLAAC/RA vs DHCPv6 addressing modes.
- Identify the header changes vs IPv4 and why (checksum gone, no fragmentation in
  routers, fixed 40-byte header).
- Work comfortably in a dual-stack network and capture/interpret both families.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-06 handout

## Homework / preparation for next lecture
- LAB-06 report due. Skim KR §5.1–5.2 (routing intro) — routing module next.
