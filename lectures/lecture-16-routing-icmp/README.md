# Lecture 16 — Routing Fundamentals & ICMP

| Field | Value |
|---|---|
| Module | 3 — Internetworking with IPv4/IPv6 |
| Depends on | L12 (IP model), L13 (prefixes), L14–L15 |
| CLOs addressed | **CLO3, CLO4** (primary), CLO6 (alternatives evaluation) |
| Bloom level | C3–C4 |
| Assessment artifact | Lab report (LAB-07); **midterm in lecture**; CS-02 due |
| Lab | LAB-07: static routing + traceroute dissection (3-router VM topology) |
| Readings | KR §4.3 (recap), §5.1–5.2 (intro); PD §3.3.2 |
| Prerequisites | L12–L15 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-07 handout (labs/) |

## Key questions
- What is inside a router's forwarding table, and how does a packet actually choose a
  next hop?
- How do routers *learn* what they forward — statically, or from each other?
- What is ICMP for beyond `ping`, and how does traceroute really work?

## What you should be able to do afterwards
- Explain forwarding vs routing and longest-prefix match with worked examples.
- Configure static routes on a multi-router topology and verify path selection.
- Compare distance-vector vs link-state approaches at concept level.
- Explain ICMP echo/unreachable/time-exceeded and traceroute's TTL mechanism.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-07 handout

## Assessment in this lecture
Midterm (90 min, Modules 1–3) runs in the first 90 minutes; LAB-07 briefing follows.
CS-02 deliverable is due (submitted before class).

## Homework / preparation for next lecture
- LAB-07 report due at L17. Read KR §3.1–3.3 (transport, UDP) — Module 4 begins.
