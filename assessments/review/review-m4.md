# Module 4 Review Questions (L17–L20)

| Field | Value |
|---|---|
| Coverage | L17 UDP & sockets · L18 TCP connections & reliability · L19 flow & congestion control · L20 reliable transport over UDP (project) |
| Use | Self-study after each lecture; answers in the key below |
| Links | Lecture packages: [`../../lectures/`](../../lectures/) · LAB-08…LAB-11 · Cases PB-033…PB-040 |

## Questions

### L17 — UDP & sockets
1. [B|CLO4] UDP header: name its four fields and what breaks if checksum is disabled
   (accept: what it protects against).
2. [I|CLO4] DNS uses port 53 for both queries and responses. Which side binds which,
   and what does the client's ephemeral port accomplish?
3. [I|CLO5] Write pseudocode for a UDP echo server loop (recvfrom/sendto) and state
   what state it keeps between packets.

### L18 — TCP connections & reliability
4. [I|CLO4] Why does SYN consume a sequence number but a pure ACK not? What breaks
   otherwise?
5. [I|CLO4] Byte stream 1–1000 sent; segments 501–1000 arrive first. What does the
   receiver do with them and with its ACK?
6. [I|CLO4] Define RTO's inputs (RTT samples, srtt, rttvar) and the failure each
   component prevents.

### L19 — TCP flow & congestion control
7. [B|CLO4] What two windows bound a sender's in-flight data, and whose interest does
   each protect?
8. [I|CLO5] BDP calculation: 1 Gb/s, 40 ms RTT. What receiver window keeps the pipe
   full?
9. [I|CLO4] Slow start vs congestion avoidance: what triggers the transition, and what
   does cwnd do in each?
10. [I|CLO6] Fast retransmit fires after three duplicate ACKs. Why three, in the
    course's simplified account?

### L20 — Reliable transport over UDP (project)
11. [I|CLO5] Your protocol's state machine: list the states for one direction of a
    transfer (idle → sending → closing) and the event that exits each.
12. [I|CLO5] Sliding window over UDP: what does the sender track per unacked byte, and
    what does an out-of-order arrival do at the receiver?
13. [I|CLO6] Your project hits 5 Mb/s on a 100 Mb/s netem link with 2% loss. Which
    mechanism (window, RTO policy, or ACK scheme) is the first suspect, and why?
14. [I|CLO6] Compare your protocol's timeout decision to TCP's: one similarity, one
    divergence, and the cost of the divergence.

---

## SELF-CHECK KEY — attempt first, then verify

1. Source port, destination port, length, checksum. Disabled checksum loses
   corruption detection for header+data — silent data corruption reaches apps.
2. Server binds 53 (its listening socket); client sends from an ephemeral port so
   replies return to the right query — and concurrent queries don't collide.
3. `while True: data, addr = s.recvfrom(65535); s.sendto(data, addr)` — stateless:
   no per-client state between packets (that's the point of UDP).
4. SYN consumes one seq number so the handshake ACKs (and retransmits of SYN) are
   distinguishable from data bytes; otherwise a retransmitted SYN could be mistaken
   for a data byte and the stream would mis-align.
5. Receiver buffers 501–1000 (out-of-order hold) and ACKs 501 ("next expected byte");
   when 1–500 arrives, one cumulative ACK of 1001 confirms all.
6. srtt = smoothed RTT estimate; rttvar = variability estimate; RTO = srtt + 4·rttvar.
   srtt prevents firing too early on average paths; rttvar prevents spurious fires on
   jittery paths; without adaptation a fixed timer either retransmits early (waste) or
   waits long (idle stalls).
7. cwnd (sender's congestion view) and rwnd (receiver's advertised space). cwnd
   protects the network; rwnd protects the receiver's buffer.
8. BDP = 10⁹ × 0.04 = 4×10⁷ bits = 5 MB [MC] — window ≥ 5 MB.
9. Transition at cwnd ≥ ssthresh; slow start: exponential growth per RTT; avoidance:
   linear (+1 MSS per RTT).
10. Three duplicates mean three *later* segments arrived, so the first segment's loss
    is likely (not reordering): retransmit without waiting for the RTO.
11. IDLE —(start transfer)→ SENDING —(all bytes acked)→ CLOSING —(final ACK/timeout)→
    closed. Accept equivalent named machines with correct triggers.
12. Sender: per-byte or per-segment send time + retransmit deadline (or a bitmap);
    receiver: out-of-order arrivals are buffered and a selective/cumulative ACK
    reports the gap.
13. Window first: at 2% loss, RTO-driven stalls amplify any window shortfall; compute
    implied window = rate×RTT and compare to configured window before touching timers.
14. Similarity: timeout on unacked data → retransmit. Divergence: course projects
    typically use fixed timers (no srtt/rttvar) — cost: spurious retransmits on
    jittery paths or slow recovery after real loss.
