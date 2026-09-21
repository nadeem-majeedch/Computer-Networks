# Lecture 09 — VLANs & L2 Segmentation

| Field | Value |
|---|---|
| Module | 2 — Physical & Data Link Foundations |
| Depends on | L07–L08 (frames, switching, broadcast domains) |
| CLOs addressed | **CLO2** (primary), CLO6 (segmentation trade-offs), CLO7 (security benefit) |
| Bloom level | C3–C4 |
| Assessment artifact | Lab report (LAB-02) |
| Lab | LAB-02: build a switched lab with VLANs (VM/simulator, pairs) |
| Readings | PD §3.2 (VLAN section, ⚠ verify); IEEE 802.1Q (concept) |
| Prerequisites | L08 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-02 handout (labs/) |

## Key questions
- How can one physical switch behave like several isolated switches?
- What exactly travels across a trunk link, and how does the receiving switch know
  which VLAN a frame belongs to?
- When is L2 segmentation the right tool — and when do you need L3 instead?

## What you should be able to do afterwards
- Explain VLAN purpose, 802.1Q tagging, access vs trunk ports.
- Predict which frames cross a trunk and how tags are added/removed.
- List inter-VLAN routing options and their trade-offs.
- Argue the security benefits *and* limits of VLANs (they are not firewalls).

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-02 handout

## Homework / preparation for next lecture
- LAB-02 report due next week. Read PD §2.7 (wireless intro) and note your home Wi-Fi's
  band and channel if you can find it.
