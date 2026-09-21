# LAB-08 Worksheet

Names (pair): ________________  ______  Date: ______  Environment table: ______

## Pre-lab
1. Demux key for `*:5000`: ______________________
2. UDP header = ____ bytes: ______, ______, ______, ______
3. Missing rung + app where UDP is right: ______________________

## T0/T1 — First capture record
| Field | Value from your capture |
|---|---|
| client port (ephemeral) | |
| server port | |
| payload (ASCII) | |
| handshake packets seen | |

"Connectionless" in one line, from your capture: ______________________

## T2 — Format
Payload format chosen: `__________________`
If packet 2 is lost, current protocol does: ______________________

## T3 — ACK protocol log
| Attempt | sent seq | ack received? | timeout? |
|---|---|---|---|
| server alive | | | |
| server killed | | | |
| attempts observed before clean failure: ____ (expected: 3) |

## T4 — ICMP side effect
Capture line (paste): ______________________
Client exception/behavior: ______________________

## Post-lab (full answers in report)
1. Demux key + why the reply found the client
2. Two rungs added, one still missing (L17 ladder)
3. Why `recvfrom`'s address suffices for the reply
4. Is port-unreachable a reliability guarantee? Why not?
