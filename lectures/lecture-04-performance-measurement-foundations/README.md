# Lecture 04 — Performance Lab Foundations: Measuring the Network

| Field | Value |
|---|---|
| Module | 1 — Foundations & Architecture |
| Depends on | L01 (delay/throughput vocabulary), L02 (basic tooling) |
| CLOs addressed | **CLO4, CLO5** (primary), CLO6 (introduced) |
| Bloom level | C3–C4 |
| Assessment artifact | LAB-01 worksheet (estimates vs measurements) |
| Lab | LAB-01: measure & interpret latency/throughput with `ping`, `traceroute`, `iperf3` |
| Readings | KR §1.4 (recap); PD §1.5 (perspective); tool man pages |
| Prerequisites | L01–L03; course VM installed |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · slides.md (pending later pass) |

## Key questions
- How do you turn "the network feels slow" into a measured, defensible statement?
- What can `ping`, `traceroute`, and `iperf3` each tell you — and what can they *not*?
- Why must every measurement carry units, context, and a reproducible command?

## What you should be able to do afterwards
- Estimate a transfer time *before* measuring it (delay + bandwidth math from L01).
- Use `ping`, `traceroute`, `iperf3` correctly and interpret their output with caveats.
- Explain measurement pitfalls: ICMP rate-limiting, load-dependent RTT, single-stream
  throughput vs path capacity.
- Produce a lab report that another person could reproduce exactly.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-01 handout (labs/)

## Homework / preparation for next lecture
- Submit LAB-01 worksheet. Read PD §2.1–2.2 (physical layer intro) — Module 2 begins.
