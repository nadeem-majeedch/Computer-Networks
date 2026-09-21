# Lecture 01 — What Is a Network? Overview, History & the Internet Today

| Field | Value |
|---|---|
| Module | 1 — Foundations & Architecture |
| Depends on | None (first lecture) |
| CLOs addressed | **CLO1** (primary), CLO4, CLO5 (introduced) |
| Bloom level | C1–C2 |
| Assessment artifact | Exit ticket; in-lecture worksheet (delay types & calculations) |
| Lab | GA-01: guided Wireshark tour on a pre-captured trace |
| Readings | KR ch. 1 (§1.1–1.5); PD ch. 1 (§1.1–1.3) |
| Prerequisites | None beyond [`prerequisites.md`](../../docs/prerequisites.md) entry skills |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · slides.md (pending later pass) |

## Key questions
- What exactly makes a set of connected computers a *network*?
- Why does the Internet use packet switching instead of circuit switching?
- Where does time go when data crosses the Internet, and why can't we "make latency zero"?
- Who runs the Internet, and what does its structure look like?

## What you should be able to do afterwards
- Define a computer network and distinguish circuit switching from packet switching.
- Name and compute the four delay components (processing, queueing, transmission, propagation).
- Distinguish bandwidth, throughput, latency/RTT, jitter, and loss — with correct units.
- Sketch the structure of the modern Internet: access networks, ISPs, IXPs, CDNs.
- Open a packet trace in Wireshark, apply a display filter, and identify the frame/packet/segment hierarchy.

## Materials
- [Teaching notes](notes.md) — instructor-facing, includes demo commands and answer keys
- [Worksheet](worksheet.md) — in-lecture activity + exit ticket
- Traces: any small HTTP capture from the [Wireshark SampleCaptures page](https://wiki.wireshark.org/SampleCaptures), or one captured on the course VM

## Homework / preparation for next lecture
- Read KR ch. 1 §1.5 (protocol layers) and note one question about "layers" to bring to L02.
- Install Wireshark on your laptop if not already present.
