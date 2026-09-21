# Lecture 19 — Worksheet & Exit Ticket

Name: ________________  Date: ______

## Part A — Window math (8 min)
1. rwnd = 64 KB, RTT = 100 ms → max throughput = ________ Mbps
2. To fill 1 Gbps × 50 ms you need a window of ________ MB (BDP).
3. cwnd = 200 MSS on RTT 40 ms, MSS 1460 B → throughput ≈ ________ Mbps
4. Which of rwnd/cwnd binds in Q1? ________ In Q3? ________

## Part B — Loss events (7 min)
5. cwnd = 200 MSS; loss signaled by 3 dup-ACKs → ssthresh = ________, cwnd ≈ ________
6. Same cwnd; loss signaled by RTO timeout → ssthresh = ________, cwnd = ________
7. After event 5, growth resumes at ________ MSS per ________.

## Part C — Bufferbloat (5 min)
8. 10-Mbps link, 4-MB buffer, queue full → added delay = ________ s
9. Two fixes (named in class): ________ / ________

## Exit ticket (3 items)
1. Throughput = min( ______ , ______ ) / ______
2. Timeout loss: cwnd ________ ; dup-ACK loss: cwnd ________.
3. BDP = ________
