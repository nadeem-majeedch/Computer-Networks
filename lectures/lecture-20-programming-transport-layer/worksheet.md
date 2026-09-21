# Lecture 20 — Project Spec Template & Exit Ticket

Pair: ________________  Date: ______  **Spec due at end of session**

## §1 Goal & reliability definition
- Application: (file transfer / chat / other) ________
- "Reliable" means (name exactly what must hold): ________
- Rungs included: ☐ seq ☐ ACK ☐ timeout/retransmit ☐ in-order ☐ window/bonus

## §2 Chunk format
| Field | Size | Purpose |
|---|---|---|
| type | | |
| seq | | |
| len | | |
| payload | ≤1,400 B | |

## §3 State diagrams (draw; both endpoints)
Sender states: ________ → ________ → ________
Receiver states: ________ → ________

## §4 Timers
| Timer | Value | Action on expiry |
|---|---|---|
| RTO | | |

## §5 Edge cases (≥5, from the workshop list)
1. Loss rate = 0% but ACKs arrive reordered — what breaks if I trust duplicate-ACK count alone?
2. Chunk arrives twice (retransmit raced with ACK) — how does the receiver suppress the duplicate?
3. Acknowledgment for chunk n is lost — which side acts, and on what timer?
4. Receiver dies mid-transfer — when does the sender notice, and what should it do?
5. Chunk larger than the buffer the receiver advertised — prevented by which design rule?

## §6 Evaluation matrix (≥6 cells, with predictions)
| Loss | Delay/reorder | File | Predicted time | Predicted retransmits |
|---|---|---|---|---|
| 0% | none | 1 MB | | |
| 2% | none | 1 MB | | |
| 5% | 50 ms ± 25 | 1 MB | | |

## Exit ticket (submission checkpoint)
1. My reliability definition (what the receiver must guarantee): ________
2. Rungs I skipped and why the failure model made them unnecessary: ________
3. The evaluation-matrix cell I most fear, and the rung I would add first: ________
