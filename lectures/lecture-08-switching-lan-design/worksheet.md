# Lecture 08 — Worksheet (GA-08) & Exit Ticket

Name: ________________  Date: ______

Topology for all parts (same as board):

```
A[p1]─SW1[p1..p4]══link══SW2[p1..p2]─C[p1]      (B[p2 on SW1], D[p2 on SW2] idle)
```

## Part A — FDB prediction (pairs, 15 min)
Fill each switch's FDB (MAC→port) **after** each event; then state the forwarding
decision (forward / flood / filter) and out-ports.

| # | Frame | SW1 FDB | SW2 FDB | Decision(s) |
|---|---|---|---|---|
| 1 | A→C | | | |
| 2 | C→A | | | |
| 3 | A→C | | | |
| 4 | B→A | | | |
| 5 | D→B | | | |

## Part B — Reasoning (7 min)
6. Why did frame 2 teach SW1 a *new* entry even though A was already known? ________
7. A frame arrives at SW1 destined for MAC-D. Decision? Why? ________
8. Host C is unplugged and replugged on SW2 p2 an hour later. Any stale-entry effect?
   For how long could traffic to C flood? ________

## Part C — Design (8 min)
9. Management wants a second link between SW1 and SW2 for "backup speed". What must be
   true for this not to cause an outage? ________
10. Name three problems of one flat LAN with 500 hosts (CS-02 seed): ________

## Exit ticket (3 items)
1. Learn reads the ________ MAC; lookup reads the ________ MAC.
2. Unknown unicast → ________.
3. STP prevents ________.
