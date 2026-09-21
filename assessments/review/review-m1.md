# Module 1 Review Questions (L01–L04)

| Field | Value |
|---|---|
| Coverage | L01 networks & delay taxonomy · L02 layering · L03 applications/sockets · L04 measurement |
| Use | Self-study after each lecture; answers in the key below — attempt first |
| Links | Lecture packages: [`../../lectures/`](../../lectures/) · Practice cases: PB-001…PB-008 |

## Questions

### L01 — What is a network?
1. [B|CLO1] Define a computer network in one sentence that includes *why* networks
   exist (what they enable beyond connecting two machines).
2. [B|CLO1] List the four delay components of the taxonomy and name one physical or
   system cause of each.
3. [I|CLO1] A game studio chooses packet switching for multiplayer. Name two properties
   of packet switching that fit that workload.
4. [I|CLO1] Distinguish bandwidth, throughput, and goodput in one sentence each.

### L02 — Layered architectures
5. [B|CLO1] Why does layering help different vendors build interoperable products?
   One sentence, naming the interface concept.
6. [B|CLO1] A frame carries an HTTP response. List the encapsulation chain from the
   HTTP message down to bits on copper.
7. [I|CLO1] Give one real cost of layering (a behavior layering makes harder) and name
   the class of designs that deliberately cross layers.
8. [I|CLO1] Which standards body would publish a new Ethernet speed, and which a new
   version of TCP? Why the split?

### L03 — Applications, sockets & the packet's journey
9. [B|CLO1] What does a port number identify, and why do well-known ports exist?
10. [I|CLO4] Trace a first-time `https://example.com` fetch through every layer at the
    client, naming the PDU handed down at each step.
11. [I|CLO4] A client cache hit skips which of: DNS, TCP, TLS, HTTP? What assumption
    makes the skip safe?
12. [I|CLO1] Client–server vs P2P: give one workload where each is the natural fit and
    the reason.

### L04 — Performance, measurement & QoS foundations
13. [B|CLO5] Write the definition of RTT and name the tool class that measures it.
14. [I|CLO5] `iperf3` reports 94.2 Mb/s on a "100 Mb/s" link. Give two defensible
    explanations and state which artifact proves each.
15. [I|CLO5] Why is a single ping an unreliable capacity or health signal? Name the
    measurement principle.
16. [I|CLO6] A backup window needs 500 GB moved in 4 h. Minimum sustained throughput?
    State assumptions.

---

## SELF-CHECK KEY — attempt first, then verify

1. An interconnected set of devices exchanging data via agreed protocols — enabling
   resource sharing, communication, and distributed services across distance.
2. Transmission/serialization (link speed, frame size) · propagation (distance ÷ signal
   speed in medium) · queueing (buffer occupancy under load) · processing (per-hop
   lookup/parse cost).
3. No dedicated circuit to waste between bursts; graceful behavior when paths/nodes
   fail (packets reroute). Accept statistical-multiplexing efficiency for bursty traffic.
4. Bandwidth = capacity of the link; throughput = bits actually delivered per second;
   goodput = useful payload bits/s excluding headers/retransmits.
5. Each layer publishes a stable interface, so independent implementers only need to
   agree on interfaces, not internal design.
6. HTTP message → TCP segment (ports, seq) → IP datagram (addresses, TTL) → Ethernet
   frame (MACs, FCS) → physical symbols/bits.
7. Example: performance optimizations that read transport state at the application
   boundary, or scheduling that must know both link and flow context — the class is
   *cross-layer* design.
8. IEEE (802.3 working group) for Ethernet; IETF (RFC process) for TCP — each owns its
   layer's specifications.
9. The application endpoint inside a host; well-known ports give standard rendezvous
   points so clients can find services without configuration.
10. Browser builds HTTP request (message) → TLS wraps it (record) → TCP segment (ports,
    seq) → IP datagram (src/dst IP, TTL) → Ethernet frame (MACs, FCS) → NIC symbols.
11. DNS (and usually TCP+TLS if the connection is reused). Safe assumption: the cached
    name→IP mapping is still within TTL and the connection is still alive.
12. Client–server: controlled, consistent service (web, banking). P2P: content
    distribution scaling with peers (file sharing, some CDNs' origins) — capacity grows
    with demand.
13. RTT = time from request emission to response arrival; measured by ping-class tools
    (ICMP echo) or app-level probes.
14. (i) Protocol overhead (headers/ACKs) — provable by counting iperf3's reported
    bytes vs link rate; (ii) flow/window limits — provable by raising window size and
    re-measuring. Accept duplex mismatch with its counter evidence.
15. Single-sample statistics: queueing jitter means one probe may catch an empty or
    full buffer — principle: baseline over distributions, not points.
16. 500 GB = 4×10¹² bits ÷ (4×3600 s) ≈ 278 Mb/s sustained [MC]. Assumptions: no
    competing traffic, no per-file round-trip stalls (single large stream).
