# LAB-10 Worksheet

Names (pair): ________________  ______  Date: ______  Spec due: before LAB-11 coding

## Pre-lab
1. TCP rungs in order: ______________________
2. Why reorder tolerance is required (LAB-09 T4): ______________________
3. Stop-and-wait on 50 ms link, one number: ______________________

## T1 — Reliability definition
Guarantee sentence (testable): ________________________________________
| Rung | Implement? | One-line justification |
|---|---|---|
| per-packet ACK | | |
| timeout retransmit | | |
| ordering | | |
| dedup | | |
| flow control | | |
| congestion control | | |

## T2 — Protocol mechanics
Header fields: ______________________________ (sizes/why unambiguous: __________)
Sender states: ______ → ______ → ______ ; Receiver states: ______ → ______
Timeout value ______ ms ; justification (from measurement): ______________
Termination rule: ______________ ; defense: ______________________

## T3 — Evaluation matrix (predictions; 1 MB, 50 ms RTT, 10 Mbit/s)
| Loss / reorder | Predicted time | Predicted retransmits |
|---|---|---|
| 0%, none | | |
| 2%, none | | |
| 5% + 50 ms ± 25 ms | | |

ACK-path assumption check: are your ACKs lossless? ______ If yes, why is that OK? ____

## T4 — Red-team record (from the reviewing pair)
Q1: ________________________________________
Q2: ________________________________________
Our answers / spec amendments: ______________________________

## Post-lab (append to spec)
1. Rejected rung + the workload that would make it wrong
2. Hardest question + why the spec survives
3. Possible deadlock + the fix
