# Lecture 29 — Monitoring, Telemetry & Systematic Troubleshooting

| Field | Value |
|---|---|
| Module | 7 — Operations, Cloud & SDN |
| Depends on | L01 (performance metrics), L16 (ICMP), L27 (LB health checks preview) |
| CLOs addressed | **CLO7** (primary), CLO1 (measurement rigor) |
| Bloom level | C2–C4 (diagnosis, evaluation) |
| Assessment artifact | Exit ticket; GA-29 monitoring dashboard; LAB-14 (capstone ops) |
| Lab | GA-29 (in-lecture); LAB-14 (capstone monitoring) |
| Readings | PD §13 (selected); monitoring survey notes (⚠ instructor-assigned) |
| Companion | [`notes.md`](notes.md) · [`worksheet.md`](worksheet.md) |
| Status | Draft v0.1 — awaiting instructor review |

## Learning outcomes
By the end, students can:
1. Choose the right measurement for a question (availability, latency,
   utilization, error) and name its limits (C3/C4).
2. Run and interpret active probes (ping, traceroute, HTTP checks) and read
   passive counters (SNMP, interface stats, LB health) (C3).
3. Build a minimal monitoring dashboard and state an alerting threshold with
   justification (C3/C5).
4. Diagnose a staged failure using layered evidence (C4/C6).

## Package contents
- `README.md` — this overview.
- `notes.md` — 120-minute instructor plan.
- `worksheet.md` — GA-29 dashboard build + exit ticket.
