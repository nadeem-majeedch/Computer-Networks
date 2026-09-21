# Lecture 07 — MAC Protocols & Wired LANs: Ethernet

| Field | Value |
|---|---|
| Module | 2 — Physical & Data Link Foundations |
| Depends on | L05–L06 (media, framing/errors) |
| CLOs addressed | **CLO2** (primary), CLO4 (frame analysis) |
| Bloom level | C2 |
| Assessment artifact | Exit ticket; GA-07 Ethernet frame-dissection worksheet |
| Lab | GA-07 (in-lecture, Wireshark); no numbered lab |
| Readings | PD §2.6; Tanenbaum MAC chapter (⚠ verify section) |
| Prerequisites | L05–L06 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · slides.md (pending later pass) |

## Key questions
- When many hosts share one wire, who gets to talk — and how was that solved?
- Why did CSMA/CD matter for 40 years and then disappear?
- What exactly is inside an Ethernet frame, field by field?

## What you should be able to do afterwards
- Explain the multiple-access problem and the ALOHA→CSMA→switched Ethernet evolution.
- Read every field of an Ethernet II frame from a hex dump, including EtherType.
- Explain why full-duplex switched Ethernet ended the collision era.
- Relate MTU, frame size, and efficiency numerically.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md)

## Homework / preparation for next lecture
- Complete GA-07. Read PD §3.1–3.2 (switching) and think: what does a switch actually
  remember?
