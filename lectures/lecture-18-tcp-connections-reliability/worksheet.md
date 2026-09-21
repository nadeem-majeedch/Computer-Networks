# Lecture 18 — Worksheet (GA-18) & Exit Ticket

Name: ________________  Date: ______

## Part A — Sequence arithmetic (8 min)
1. Client sends seq=5000, 400 B of data → server's ACK = ________
2. Server sends seq=1000, 50 B → client's ACK = ________
3. Client sends 200→350 OK, then 300–400 is lost, then 400–450 arrives.
   Server's ACKs for the 400–450 segment: ________ (what kind of ACK?) ________
4. After the third duplicate ACK, the client resends seq ________.

## Part B — Trace dissection (pairs, 12 min)
Given the provided trace (handshake → data with one loss → fast retransmit):
5. ISN of the client: ________ of the server: ________
6. Which option in the SYN declared MSS? Value? ________
7. How many duplicate ACKs before retransmission? ________
8. Which Wireshark view shows the exchange graphically? ________

## Part C — States & teardown (5 min)
9. "Connection refused" arrives as a ________ segment.
10. A socket in TIME-WAIT for 2 minutes: why so long? ________

## Exit ticket (3 items)
1. Seq counts ________; ack=N means "send me byte ______ next".
2. Fast retransmit trigger: ________
3. RTO formula (shape): ________
