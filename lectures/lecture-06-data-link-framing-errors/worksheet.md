# Lecture 06 — Worksheet (GA-06) & Exit Ticket

Name: ________________  Date: ______

## Part A — Bit stuffing (5 min)
Flag = 01111110. Stuff after five consecutive 1s.
1. Payload: `0111111 01111110 111110000` → stuffed: ________
2. How many stuffed bits did you add? ________

## Part B — CRC by hand (pairs, 14 min)
Message M = 110101, generator G = 1011 (r = 3). Show every XOR step.

3. Codeword transmitted (M + remainder): ________
4. Flip bit 4 of your codeword; recompute the remainder: ________ (detected?)
5. Now flip TWO bits (bit 2 and bit 7) of your original codeword; recompute: ________
   Was it detected? What does this teach about CRC guarantees? ________

## Part C — Choose the mechanism (5 min)
For each, pick parity / checksum / CRC / FEC, one reason:
6. Serial keyboard link, 1 bit at a time, tiny budget: ________
7. IP header integrity check: ________
8. Ethernet frame: ________
9. Satellite link to a probe with 40-minute RTT: ________

## Exit ticket (3 items)
1. Stuffing rule (one line): ________
2. CRC = error ________ (detection/correction)?
3. Transmitted codeword from Part B: ________
