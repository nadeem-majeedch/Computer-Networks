# Weekly Quiz — Week 02 (L03, L04)

| Field | Value |
|---|---|
| Coverage | L03 — Applications, sockets & the first packet hunt · L04 — Performance lab foundations |
| Mode | Formative, ~10 min, individual, open notes |
| Graded window | — |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [B|CLO1|L03]** In one sentence each: what does a *socket* identify, and what two
pieces must a client know to connect to a server's TCP socket?

**Q2 [I|CLO5|L04]** Define RTT. A `ping` shows min/avg/max = 20.1/21.0/25.4 ms over 50
probes. Give one plausible physical cause for the max tail and one measurement pitfall
that could explain why avg > min.

**Q3 [I|CLO4|L03]** A 10 MB file crosses a 25 Mb/s bottleneck with negligible per-hop
delay. Ignoring protocol handshakes, minimum transfer time? Now add two RTTs of setup at
RTT = 40 ms. Show your working.

**Q4 [B|CLO4|L04]** In the course's labs, `iperf3` measures throughput. Why can its
reported number be lower than the link's nominal bandwidth? Give two distinct reasons.

**Q5 [I|CLO1|L03]** Order these stages of a web request for a **cache-miss** fetch, and
state which stage can be skipped on a **cache-hit**: (i) TCP handshake (ii) DNS lookup
(iii) HTTP request/response (iv) TLS handshake.

**Q6 [I|CLO5|L04]** Your baseline `ping` to a server is 21 ms avg. After a configuration
change it is 23 ms. Why is that difference **not** automatically meaningful? Name the
measurement concept from L04.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** A socket identifies one endpoint of a connection as IP address + protocol +
port. A client needs the server's IP address and its (well-known or assigned) port
number, plus the protocol (TCP here). [B·CLO1]

**Q2.** RTT = time for a small request to reach the destination and its reply to return.
Max tail: queueing behind other traffic (congestion) on any hop; also accept routing
change during the probe window. Pitfall: queuing/jitter inflating the mean — or
processing on the target host adding variable delay before reply. [I·CLO5]

**Q3.** 10 MB = 8×10⁷ bits; /25×10⁶ b/s = **3.2 s** [MC]. Setup: 2 × 40 ms = 80 ms →
**≈ 3.28 s**. Assumptions stated: no other traffic, no retransmissions, handshake
serialization negligible. [I·CLO4]

**Q4.** (i) Protocol overhead (TCP/IP headers, ACK traffic) consumes link capacity;
(ii) congestion loss/windowing limits instantaneous send rate below link rate. Also
acceptable: measurement-window effects, flow-control limits at the receiver. [B·CLO4]

**Q5.** Cache-miss order: (ii) DNS lookup → (i) TCP handshake → (iv) TLS handshake →
(iii) HTTP request/response. On a cache-hit at this client: the DNS lookup (and
typically the full TLS handshake if the connection is reused) can be skipped — accept
DNS as the required answer, connection reuse as a justified bonus. [I·CLO1]

**Q6.** Difference must exceed measurement noise/baseline variability (jitter,
sampling effects) — the L04 concept is **baseline noise vs real change**: 2 ms is within
observed max−min spread (≈5 ms), so it may be ordinary variation. Compare distributions
over sufficient samples, not single averages. [I·CLO5]
