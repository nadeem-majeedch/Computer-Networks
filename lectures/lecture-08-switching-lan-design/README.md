# Lecture 08 — Switching & LAN Design

| Field | Value |
|---|---|
| Module | 2 — Physical & Data Link Foundations |
| Depends on | L07 (frames, MAC addressing, hub vs switch) |
| CLOs addressed | **CLO2** (primary), CLO6 (design reasoning) |
| Bloom level | C2–C3 |
| Assessment artifact | Exit ticket; GA-08 FDB-prediction worksheet |
| Lab | GA-08 (in-lecture); no numbered lab |
| Readings | PD §3.1–3.2 |
| Prerequisites | L06–L07 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · slides.md (pending later pass) |

## Key questions
- What does a switch actually *do* with a frame, step by step?
- How does it learn where every MAC address lives without being told?
- What breaks when the topology has loops — and how does the network cope?

## What you should be able to do afterwards
- Walk a frame through a switch: receive → learn → look up → forward/filter/flood.
- Predict a switch's forwarding database (FDB) after a given traffic sequence.
- Distinguish collision domains from broadcast domains in a multi-switch design.
- Explain why loops are dangerous at L2 and what STP is *for* (mechanics is enrichment).

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md)

## Homework / preparation for next lecture
- Complete GA-08. Read PD §3.2 (VLAN section of your edition) and list two problems a
  flat LAN causes.
