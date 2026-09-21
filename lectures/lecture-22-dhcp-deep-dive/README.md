# Lecture 22 — DHCP Deep Dive, BOOTP & Address Management

| Field | Value |
|---|---|
| Module | 5 — Application Layer & Network Services |
| Depends on | L14 (DHCP DORA, NAT), L17 (UDP) |
| CLOs addressed | **CLO4** (primary), CLO3 (address management), CLO7 (starvation attacks) |
| Bloom level | C3–C4 |
| Assessment artifact | Exit ticket; DORA annotated trace (GA-22) |
| Lab | GA-22: dissect DORA on a live capture; small IPAM exercise |
| Readings | KR §4.4.5 (revisit); RFC 2131 (selected sections); RFC 1533-era options context (via 2131) |
| Prerequisites | L14 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · slides.md (pending later pass) |

## Key questions
- What is *inside* each DHCP message — field by field — and what can go wrong there?
- How do leases, reservations, scopes, and relays combine at campus scale?
- How does "anyone can answer" become an attack, and what do admins deploy against it?

## What you should be able to do afterwards
- Read every field of a DORA exchange from a capture, including options.
- Design a small IP addressing/management plan (scopes, reservations, leases).
- Explain DHCP starvation and rogue-server attacks plus their defenses (snooping).
- Place BOOTP and PXE in DHCP's history (one slide of lineage).

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md)

## Homework / preparation for next lecture
- Complete GA-22. Read KR §2.2–2.3 (HTTP) and §2.5 — L23's protocol trio begins;
  CS-03 opens next session.
