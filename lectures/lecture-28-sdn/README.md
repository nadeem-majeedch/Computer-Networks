# Lecture 28 — Data-Plane & SDN: Programmable Networks

| Field | Value |
|---|---|
| Module | 7 — Operations, Cloud & SDN |
| Depends on | L08 (switch learning), L16 (routing), L27 (virtualization) |
| CLOs addressed | **CLO6** (primary), CLO2 (architecture) |
| Bloom level | C2–C3, evaluation (architecture trade-offs) |
| Assessment artifact | Exit ticket; GA-28 controller exercise |
| Lab | GA-28 (in-lecture); no numbered lab |
| Readings | PD §4.3 (SDN sections); OpenFlow paper (⚠ verify citation) |
| Companion | [`notes.md`](notes.md) · [`worksheet.md`](worksheet.md) |
| Status | Draft v0.1 — awaiting instructor review |

## Learning outcomes
By the end, students can:
1. Sort network behaviors into control, data, and management planes (C2).
2. Explain SDN's separation of planes and the controller–switch interface
   (flow-table model) (C2/C3).
3. Write flow-table rules for simple reachability and policy goals (C3).
4. Contrast SDN with distributed routing and name where each wins (C4/C5).

## Package contents
- `README.md` — this overview.
- `notes.md` — 120-minute instructor plan.
- `worksheet.md` — GA-28 flow-rule exercises + exit ticket.
