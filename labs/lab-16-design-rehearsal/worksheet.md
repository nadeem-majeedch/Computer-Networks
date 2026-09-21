# LAB-16 Worksheet (optional; recognition only)

Name(s): ________________  ______  Date: ______

## Pre-lab
1. Four design steps in order: ______________________
2. My headroom rule: ______________________
3. CS-04 failure mode I claim to survive: ______________________

## T1 — Requirements triage
Vague card → testable rewrite (the two flagged ones): ______________________

## T2 — Building C design
| Function | Requirement ×headroom | CIDR | Usable |
|---|---|---|---|
| staff | | | |
| guests | | | |
| servers ×3 tiers | | | |
| uplinks | | | |
VLAN map: ______________ Zone policy (one paragraph in report): ______________
Summary route: ______ (exact cover? ☐)

## T3 — Programmatic verification
Script output (paste both if you fixed a failure):
```
(first run)
(final run)
```
What the machine caught that my eyes missed: ______________________

## T4 — Prototype slice
Slice chosen: ☐ guest isolation ☐ uplink failover
Claimed property: ______________________ Test: ______________________
Evidence (paste): ______________________ What this does NOT prove: ______________

## T5 — Peer defense scoresheet (reviewer fills)
| Dimension | Evidence noted (not adjectives) | Score 1–4 |
|---|---|---|
| Requirements met | | |
| Zones defensible | | |
| Failure mode tested | | |
| Justification discipline | | |

## Post-lab (findings page)
1. Rejected requirement + negotiated rewrite
2. What the machine caught
3. Property/test/evidence + its limit
4. Weakest rubric dimension + fix plan
