# Lecture 17 — Worksheet & Exit Ticket

Name: ________________  Date: ______  Pair: ________________

## Part A — Demux reasoning (7 min)
1. Host 10.0.0.5 runs two apps both sending to server 443. Kernel gives them source
   ports 51000 and 51001. For TCP, why is there no reply confusion? ________
2. Same scene but UDP to port 53 from both apps. What distinguishes the two
   conversations? ________
3. A UDP datagram arrives with Length = 5. Verdict? ________

## Part B — Header math (5 min)
4. IP payload 1,500 B, UDP: data bytes = ________; checksum covers
   (pseudo-header + header + data)? ________
5. Why does the pseudo-header include IPs but is never transmitted? ________

## Part C — Transport choice (8 min)
App: choose TCP / UDP / UDP+self-built-reliability, with two criteria each:
6. Bank transaction: ________
7. Live voice call: ________
8. DNS query: ________
9. Game state updates at 30 Hz: ________
10. Video-on-demand download: ________

## Exit ticket (3 items)
1. UDP demultiplexing on a receive socket uses the key (IP dst, ________, IP src, ________).
2. The UDP header is ________ bytes long.
3. One rung of the reliability ladder that UDP omits (and its consequence): ________.
