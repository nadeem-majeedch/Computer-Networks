# Weekly Quiz — Week 01 (L01, L02)

| Field | Value |
|---|---|
| Coverage | L01 — What is a network? · L02 — Layered architectures: OSI & TCP/IP |
| Mode | Formative, ~10 min, individual, open notes |
| Graded window | — |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [B|CLO1|L01]** Give one sentence distinguishing *circuit switching* from *packet
switching*, and name one property each makes possible.

**Q2 [B|CLO1|L01]** A file transfer shows 100 ms one-way delay that never varies and
0% loss, yet the transfer stalls every few seconds. Which delay/loss taxonomy term best
fits the stalls, and which device behavior usually causes it?

**Q3 [I|CLO1|L01]** Link = 100 Mb/s, but a 1500 B frame also suffers 1 ms propagation
and 0.2 ms queueing. What is the *serialization (transmission) delay* of the frame, and
the *total* one-way delay? State your assumptions.

**Q4 [B|CLO1|L02]** Name the PDU at each of the four TCP/IP layers that carry user data
(application, transport, internet, link), and state one field each layer adds.

**Q5 [B|CLO1|L02]** In one sentence: why do standards bodies (IEEE, IETF) matter to
interoperability, and which body standardizes Ethernet vs IP?

**Q6 [I|CLO1|L02]** A student claims "the TCP/IP model has exactly four layers because
the link layer handles everything below the internet layer." Identify the simplification
and give the more defensible description used in this course.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** Circuit switching reserves an end-to-end path before transfer (enables bounded,
dedicated per-connection capacity, e.g., classic telephony); packet switching forwards
independent packets store-and-forward (enables statistical multiplexing and resilience
to path failure). [B·CLO1]

**Q2.** Jitter/stalls from *queueing* delay — typically an overloaded buffer (e.g., a
congested uplink) rather than distance-driven propagation. Accept "queueing delay,
buffer congestion." [I·CLO1]

**Q3.** Serialization = 1500×8 / 100×10⁶ = 12 000 / 10⁸ s = **120 µs** [MC]. Total = 120 µs
+ 1 ms + 0.2 ms ≈ **1.32 ms** (one-way). Assumption: no per-hop processing beyond stated,
no retransmissions. [I·CLO1]

**Q4.** Application: *message* (e.g., HTTP headers); Transport: *segment* (ports, seq/ack);
Internet: *datagram/packet* (IP addresses, TTL); Link: *frame* (MAC addresses, FCS/CRC).
Any correct field per layer accepted. [B·CLO1]

**Q5.** Open standards let multi-vendor equipment interoperate; IEEE standardizes
Ethernet (802.3), the IETF standardizes IP (and TCP/UDP). [B·CLO1]

**Q6.** The four-layer book view hides real structure: below IP there are distinct
sub-layers (e.g., LLC/MAC in 802 standards; physical media below that), and the course
uses the five-layer TCP/IP view (physical, link, internet, transport, application) to
keep those roles visible. Accept any answer that names the five-layer view and why.
[I·CLO1]
