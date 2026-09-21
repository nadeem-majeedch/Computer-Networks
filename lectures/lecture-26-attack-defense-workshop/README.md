# Lecture 26 — Attack & Defense Case Workshop

| Field | Value |
|---|---|
| Module | 6 — Network Security |
| Depends on | L12 (ARP), L18 (TCP/SYN), L21 (DNS), L22 (DHCP), L24–L25 (defenses) |
| CLOs addressed | **CLO7** (primary), CLO4 (evidence analysis), CLO6 (defense evaluation) |
| Bloom level | C5 |
| Assessment artifact | Workshop defense plan; **CS-03 diagnosis due** |
| Lab | GA-26: benign SYN-flood pattern emulation + defense (VM lab only) |
| Readings | Instructor notes (this package); RFC 2131 (DHCP defense context); BCP 38 (named) |
| Prerequisites | L12, L18, L21, L22, L24–L25; **ethics gate signed** |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · CS-03 materials (case-studies/) |

## Key questions
- For each attack this course has met, what does the *evidence* look like in a
  capture, and what layered defense reduces the risk to acceptable?
- How do you reason about *residual risk* when no defense is perfect?
- What does an incident-response first hour look like?

## What you should be able to do afterwards
- Match each attack to its capture signature and its layered defenses.
- Write a defense plan with justified residual risk.
- Execute the GA-26 benign emulation + defense cycle in the VM lab.
- Submit CS-03's diagnosis from real evidence.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md) · CS-03 bundle-2

## Ethics gate
All emulation runs **only** inside course VMs against course targets, per the
week-1 acknowledgment. Any attempt against teaching or real networks is an
integrity violation. Restated at session start.

## Homework / preparation for next lecture
- CS-04 capstone brief assigned today (due W13). Read PD §3.4/4.3 (cloud/SDN prep).
