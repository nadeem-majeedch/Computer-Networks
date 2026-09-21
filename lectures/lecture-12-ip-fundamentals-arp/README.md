# Lecture 12 — IP Fundamentals & ARP

| Field | Value |
|---|---|
| Module | 3 — Internetworking with IPv4/IPv6 |
| Depends on | L02 (encapsulation), L07 (Ethernet), L08 (switching) |
| CLOs addressed | **CLO4** (primary), CLO2 (link-layer interaction), CLO7 (ARP security preview) |
| Bloom level | C2–C3 |
| Assessment artifact | Exit ticket; GA-12 ARP trace worksheet |
| Lab | GA-12 (in-lecture, trace analysis) |
| Readings | KR §4.3.1–4.3.2; RFC 791 (skim); RFC 826 (skim) |
| Prerequisites | L07–L08 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · slides.md (pending later pass) |

## Key questions
- What does "best-effort delivery" actually promise — and not promise?
- What is inside an IPv4 header, field by field, and why does each exist?
- How does an IP packet get delivered to the right NIC when IP and Ethernet addresses
  are completely different?

## What you should be able to do afterwards
- Read every IPv4 header field and explain its job.
- Explain the hop-by-hop delivery model and why addresses change meaning per hop.
- Walk a full ARP resolution from capture evidence, including the cache.
- State the security weakness ARP was born with (and preview its defenses).

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md)

## Homework / preparation for next lecture
- Complete GA-12. Practice binary↔dotted-decimal conversion: 10 addresses, 10 minutes
  (L13 assumes fluency).
