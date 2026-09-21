# Weekly Quiz — Week 09 (L17, L18)

| Field | Value |
|---|---|
| Coverage | L17 — UDP & sockets · L18 — TCP connections & reliability |
| Mode | Formative, ~10 min, individual, open notes |
| Graded window | — |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [B|CLO4|L17]** State the two things a transport-layer port number does for
demultiplexing, and why a datagram needs (IP, protocol, port) to find its process.

**Q2 [I|CLO4|L18]** Show the TCP three-way handshake as a sequence of packets with
sequence and acknowledgment numbers, starting from client ISN = 1000 and server ISN =
5000. Mark SYN/SYN+ACK/ACK.

**Q3 [I|CLO4|L18]** Client's first data byte carries seq 1001. The client sends 500
bytes. What ack number does the server's next ACK carry, and what does that number
*mean*?

**Q4 [I|CLO4|L17]** A telemetry app chooses UDP over TCP. Name two TCP behaviors UDP
avoids, and the cost the app accepts in exchange.

**Q5 [I|CLO4|L18]** What exactly is the retransmission timer (RTO) for, and why must it
adapt instead of being fixed at, say, 500 ms?

**Q6 [I|CLO6|L18]** A capture shows `SYN → SYN+ACK → ACK` followed by nothing for 30 s,
then a retransmitted SYN from the client. Which stage failed and give one plausible
cause consistent with the capture.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** Ports identify the sending/receiving *application endpoint* within a host and
let the OS demultiplex arriving datagrams per process. The full 3-tuple (IP, protocol,
port) is needed because two hosts may run the same port number, and TCP vs UDP port
spaces are independent. [B·CLO4]

**Q2.** Client → `SYN, seq=1000`; Server → `SYN+ACK, seq=5000, ack=1001`; Client →
`ACK, seq=1001, ack=5001`. (SYN consumes one sequence number — the +1s.) [I·CLO4]

**Q3.** ack = **1501** [MC]; it means "I have received bytes through 1500 — next byte I
expect is 1501" (cumulative acknowledgment). [I·CLO4]

**Q4.** Avoids: connection setup/teardown latency and retransmission/head-of-line
blocking on loss. Cost: the app must handle loss, duplication, and reordering itself if
it cares (e.g., its own sequencing). [I·CLO4]

**Q5.** RTO bounds how long TCP waits for an ACK before resending. It must adapt
because path RTT varies (queueing, rerouting): a fixed short timer causes spurious
retransmits on slow paths; a fixed long timer wastes time after real loss. Standard
mechanism: smoothed RTT estimate + RTT variance (state as course-level detail). [I·CLO4]

**Q6.** Failure at the **data phase**, not connection setup: the handshake completed,
then the client's data (or a keepalive-equivalent) got no ACKs — e.g., an MTU/blackhole
where the server's ACKs for larger packets never arrive, or an intermediary dropping
data-bearing packets while allowing handshake-sized ones. Any cause consistent with
"handshake OK, data stalls" earns credit. [I·CLO6]
