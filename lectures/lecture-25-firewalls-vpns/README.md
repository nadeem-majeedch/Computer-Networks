# Lecture 25 — Perimeter & Internal Defenses: Firewalls, Segmentation & VPNs

| Field | Value |
|---|---|
| Module | 6 — Network Security |
| Depends on | L24 (crypto/TLS), L09 (VLAN segmentation), L14 (NAT boundary) |
| CLOs addressed | **CLO7** (primary), CLO3 (zone addressing), CLO6 (policy evaluation) |
| Bloom level | C4–C5 |
| Assessment artifact | Lab report (LAB-13) with policy justifications |
| Lab | LAB-13: firewalls & VPN (nftables policy + site-to-site tunnel, VM pairs) |
| Readings | KR §8.4–8.9 (selected); PD §8.3 |
| Prerequisites | L24; L09, L14 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-13 handout (labs/) |

## Key questions
- What can a firewall actually decide, packet by packet, and what can it *never* see?
- Why does "deny by default, allow by exception" beat rule-pile designs?
- What does a VPN tunnel protect — and what does it deliberately not change?

## What you should be able to do afterwards
- Distinguish packet-filter vs stateful vs application-layer inspection.
- Write and justify a small nftables policy (default-drop, service allows).
- Place DMZ/zone design and IDS/IPS in defense-in-depth.
- Configure and verify a site-to-site tunnel; explain encapsulation overhead (MTU!).

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-13 handout

## Homework / preparation for next lecture
- LAB-13 report due. CS-03 diagnosis due next session — finish your evidence log.
