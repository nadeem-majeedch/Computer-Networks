# Lecture 07 — Worksheet (GA-07) & Exit Ticket

Name: ________________  Date: ______

## Part A — Frame dissection (pairs, 12 min)
Given the capture excerpt on the projector / provided hex dump:

```
ff ff ff ff ff ff | 3c 7a 8f 15 22 9c | 08 06 | <ARP payload (28 B)> | <padding>
```
1. Destination MAC: ________  Type (unicast/multicast/broadcast): ________
2. Source MAC OUI (first 3 bytes): 3c:7a:8f → vendor if shown in class: ________
3. EtherType: ________ → protocol: ________
4. Payload is 28 B. Ethernet requires ≥46 B payload. What did the sender add, and what is
   it called? ________

## Part B — Efficiency math (5 min)
5. Efficiency for a 100-byte payload (frame = payload + 14 + 4 B; count preamble 8 B on
   wire): ________ %
6. Efficiency for a 1500-byte payload: ________ %

## Part C — Hub vs switch (5 min)
7. A frame arrives destined for MAC X. Hub behavior: ________. Switch that has learned
   X on port 3: ________. Switch that has NOT learned X: ________ (preview of L08).

## Exit ticket (3 items)
1. Ethernet payload range: ________ to ________ bytes.
2. EtherType 0x0806 = ________.
3. Collision domains on an 8-port switch: ________. Broadcast domains: ________.
