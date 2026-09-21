# Lecture 21 — DNS: The Internet's Directory

| Field | Value |
|---|---|
| Module | 5 — Application Layer & Network Services |
| Depends on | L17 (UDP), L12 (addressing), L03 (application journey) |
| CLOs addressed | **CLO4** (primary), CLO7 (DNS security preview) |
| Bloom level | C3–C4 |
| Assessment artifact | Exit ticket; resolution-path worksheet (GA-21) |
| Lab | GA-21: `dig`/`nslookup` drills + capture a full resolution |
| Readings | KR §2.4; RFC 1034/1035 (skim); PD §9.3.1 (perspective) |
| Prerequisites | L12, L17; L03's journey table |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · slides.md (pending later pass) |

## Key questions
- How does a name become an address, and how *fast* — given the whole world asks?
- What do the records actually say (A, AAAA, CNAME, MX, NS, TXT)?
- Why does DNS break in weird ways (caches, negative answers, TTLs)?
- How is a *trusted* directory attacked — and what DoH/DoT/DNSSEC change?

## What you should be able to do afterwards
- Walk a full recursive/iterative resolution with the right queries at each step.
- Read record sections of a `dig` answer and explain each type present.
- Reason about TTLs and caches, including negative caching.
- Name the attack classes (spoofing/hijacking) and the concept of the DNSSEC/DoH
  responses.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md)

## Homework / preparation for next lecture
- Complete GA-21. Read KR §4.4.5 (DHCP revisit) and think: what do DHCP and DNS
  have in common?
