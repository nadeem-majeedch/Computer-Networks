# 32-Lecture Master Schedule

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Format | 32 lectures × 2 hours = 64 instructional hours |
| Status | Draft v0.1 — awaiting instructor review |
| Companions | [`syllabus.md`](syllabus.md) · [`clo-mapping.md`](clo-mapping.md) · [`lab-strategy.md`](lab-strategy.md) · [`case-study-strategy.md`](case-study-strategy.md) |

## Legend

- **Core** — required topics every student must master.
- **(enr)** — enrichment topics; may be omitted without breaking course coherence.
- **Lab / GA** — hands-on lab (`LAB-xx`, see [`lab-strategy.md`](lab-strategy.md)) or in-lecture
  guided activity. GA activities need no dedicated lab session; the 11 numbered labs are
  designed for the weekly 2-hour lab block (≈2.5 h total commitment each).
- **M&C** — minute-by-minute 120-minute pacing; see [Teaching pattern](#teaching-pattern) and
  per-module breakdowns below.
- **Bloom** — target cognitive level (C1 Remember … C6 Create); mirrors the CLO levels in
  [`learning-outcomes-clos.md`](learning-outcomes-clos.md).
- **Assessment artifact** — what students produce that measures the listed CLOs; collected per
  [`assessment-strategy.md`](assessment-strategy.md).
- **CS** — case-study milestone touchpoint (CS-01…CS-04; see
  [`case-study-strategy.md`](case-study-strategy.md)).

## Teaching pattern

Every 120-minute lecture uses the same skeleton (adapting lecture types, e.g., a lab
briefing lecture compresses the concept block):

| Segment | Minutes | Purpose |
|---|---|---|
| Recap + objectives + hook | 0–10 | Activate prior lecture; state outcomes; pose the day's driving question |
| Concept block | 10–60 | Layered theory with slides, whiteboard, and live demos |
| Break | 60–65 | — |
| Activity block | 65–110 | Live packet analysis / Python demo / worksheet / GA / lab briefing |
| Wrap-up | 110–120 | Exit ticket (2–3 quiz-style questions), preview, pointers to readings/labs |

Per-module minute allocations for the Concept and Activity blocks are given in each module
overview below.

## Master schedule

### Module 1 — Foundations & Architecture (L01–L04, 8 h)

> Concept block ≈ 75 min/lecture, activity ≈ 30 min/lecture. No prior networking assumed.
> Feeds CLO1; opens the CS-01 thread at L04.

| # | Lecture title | Core topics | Enrichment topics (enr) | Lab / GA | CS | M&C | Bloom | CLOs | Assessment artifact |
|---|---|---|---|---|---|---|---|---|---|
| L01 | What is a network? Overview, history & the Internet today | Network definition; circuit vs packet switching; delay/loss/jitter taxonomy (transmission, propagation, queueing, processing); bandwidth vs throughput; the modern Internet's shape (access/edge/core, IXP, CDN); history milestones | Switching fabric families (enr); queuing disciplines FIFO/priority (enr) | GA-01a: guided Wireshark tour on a pre-captured trace | — | 10/50/5/45/10 | C1–C2 | CLO1 | Exit ticket; in-lecture worksheet on delay types |
| L02 | Layered architectures: OSI & TCP/IP | Why layering; OSI 7 vs TCP/IP 5-layer views; encapsulation/decapsulation, PDU names, headers/trailers; hourglass model; standards bodies (ISO, IEEE, IETF/RFC, ITU, ICANN/IANA); critique of layering | Cross-layer design debate (enr); alternative layerings (enr) | GA-02: header-dissection puzzle worksheet on a real frame | — | 10/55/5/40/10 | C2 | CLO1 | Exit ticket; encapsulation worksheet |
| L03 | Applications, sockets & the first packet hunt | Application-layer anatomy (messages, client/server, P2P); sockets as the OS API; end-to-end delay & throughput math for a simple transfer; path of a web request end to end | Scaling patterns (enr); CDNs revisited (enr) | GA-03a: Python `socket` demo; GA-03b: trace the journey of one HTTP request on paper + trace | CS-01 kickoff (volcano-eruption exercise: identify "Layer 1–7" of the incident) | 10/50/5/45/10 | C2–C3 | CLO1, CLO4 | Exit ticket; GA submission |
| L04 | Performance lab foundations: measuring the network | Measurement vocabulary (latency/RTT, throughput, jitter, loss); estimation vs measurement; baselining; measurement pitfalls (sampling, observer effects) | Measurement tools beyond the course (enr) | LAB-01: measure & interpret latency/throughput with `ping`, `traceroute`, `iperf3` | CS-01 milestone 1 | 10/40/5/55/10 | C3–C4 | CLO4, CLO5 | Lab worksheet (estimates vs measurements) |

### Module 2 — Physical & Data Link Foundations (L05–L11, 14 h)

> Concept ≈ 70 min, activity ≈ 35 min per lecture. Core feeds CLO2, CLO4, CLO7; builds
> toward Module 3. Security previews begin here (L11).

| # | Lecture title | Core topics | Enrichment topics (enr) | Lab / GA | CS | M&C | Bloom | CLOs | Assessment artifact |
|---|---|---|---|---|---|---|---|---|---|
| L05 | Physical layer: signals, media & transmission basics | Signals, bandwidth (Hz), Nyquist and Shannon capacity; media: twisted pair, fiber, wireless; encoding basics; modulation overview; connectors & physical topologies | Advanced modulation (enr); optical multiplexing DWDM (enr) | GA-05: Nyquist/Shannon calculation drills | — | 10/55/5/40/10 | C2–C3 | CLO1, CLO2 | Exit ticket; calculation worksheet |
| L06 | Data link layer: framing, errors & reliability | Framing, byte/bit stuffing; error detection: parity, checksum, CRC; retransmission vs forward error correction; link reliability concepts | Hamming code walkthrough (enr); ARQ variants on a link (enr) | GA-06: compute a CRC by hand (polynomial division) | — | 10/55/5/40/10 | C3 | CLO2 | Exit ticket; CRC worksheet |
| L07 | MAC protocols & wired LANs: Ethernet | Multiple-access problem; ALOHA→CSMA/CD→switched Ethernet evolution; modern full-duplex Ethernet; Ethernet frame format (EtherType, MTU); speeds (1G→400G) | Half-duplex history & why it died (enr); jumbo frames (enr) | GA-07: dissect real Ethernet frames in Wireshark | — | 10/50/5/45/10 | C2 | CLO2, CLO4 | Exit ticket; frame-dissection worksheet |
| L08 | Switching & LAN design | Switch forwarding/learning/filtering; flooding & unknown unicast; forwarding vs filtering database; broadcast domains vs collision domains; spanning tree problem & STP concept (purpose only); uplink & hierarchy | STP/RSTP mechanics (enr); link aggregation LACP (enr) | GA-08: predict a switch's FDB from a traffic scenario | — | 10/55/5/40/10 | C2–C3 | CLO2, CLO6 | Exit ticket; FDB prediction worksheet |
| L09 | VLANs & L2 segmentation | VLAN motivation & 802.1Q tag; access vs trunk ports; inter-VLAN options; VLAN security benefits & risks; L2 vs L3 segmentation trade-offs | Private VLANs (enr); QinQ (enr) | LAB-02: build a switched lab with VLANs (virtualization or simulator) | — | 10/45/5/50/10 | C3–C4 | CLO2, CLO6 | Lab report |
| L10 | Wireless networking: Wi-Fi fundamentals | 802.11 architecture (STA, AP, BSS/ESS, DS); CSMA/CA, ACKs, hidden node; channels, 2.4/5/6 GHz; association & authentication steps; wireless performance realities (half duplex, airtime) | Wi-Fi 6/6E/7 headline features (enr); roaming (enr) | LAB-03: Wi-Fi survey with a laptop/phone + guided packet analysis of an association | — | 10/50/5/45/10 | C2–C3 | CLO2, CLO6 | Lab report |
| L11 | Wireless in practice + LAN security preview | Wireless troubleshooting patterns (interference, RSSI, airtime); wired LAN attack surface: MAC flooding, ARP problems, rogue DHCP; intro to port security & 802.1X concept | WPA2/WPA3 personal vs enterprise (enr); spectrum analysis (enr) | LAB-03 wrap: write up Wi-Fi findings | CS-02 kickoff (Meridian Systems: two-building company needs a segmented LAN) | 10/45/5/50/10 | C3–C4 | CLO2, CLO6, CLO7 | Lab write-up; CS-02 initial LAN design sketch |

### Module 3 — Internetworking with IPv4/IPv6 (L12–L16, 10 h)

> Concept ≈ 70 min, activity ≈ 35 min per lecture. The module's mathematical core is
> subnetting (L13); routing consolidates (L16). Feeds CLO3, CLO4, CLO6, CLO7.

| # | Lecture title | Core topics | Enrichment topics (enr) | Lab / GA | CS | M&C | Bloom | CLOs | Assessment artifact |
|---|---|---|---|---|---|---|---|---|---|
| L12 | IP fundamentals & ARP | IPv4 datagram format; addressing, classes→CIDR history; special addresses (private, loopback, broadcast); best-effort delivery; ARP: purpose, cache, gratuitous ARP; ARP spoofing preview (security thread) | Proxy ARP (enr); ARP history & why it's still trusted (enr) | GA-12: walk ARP resolution on a real trace | — | 10/55/5/40/10 | C2–C3 | CLO2, CLO4, CLO7 | Exit ticket; ARP trace worksheet |
| L13 | IPv4 subnetting & VLSM | Subnet masks & slash notation; computing network/broadcast/host ranges; VLSM; route aggregation & CIDR; design heuristics (growth headroom, documentation) | Binary shortcuts & speed techniques (enr) | LAB-04: subnetting drills + design exercise on a real topology | — | 10/45/5/55/10 | C3–C4 | CLO3 | Graded subnetting problem set |
| L14 | IP addressing at scale: DHCP & NAT | DHCP DORA & relay agents; lease lifecycle; NAT: many-to-one, port translation, edge cases; NAT's effects on applications; public/private addressing & registries (IANA/RIR) | CGNAT (enr); IPv4 exhaustion markets (enr) | LAB-05: configure DHCP & NAT on a Linux router (VM lab) | — | 10/50/5/45/10 | C3 | CLO3, CLO4 | Lab report |
| L15 | IPv6 | Why IPv6; address structure, types (GUA, LLA, ULA, multicast); SLAAC & RA vs DHCPv6; dual stack & transition mechanics; headers & extension headers | 6to4/Teredo history & lessons (enr); NAT64/DNS64 (enr) | LAB-06: dual-stack lab (IPv4+IPv6 VMs, capture both) | — | 10/50/5/45/10 | C3 | CLO3, CLO4 | Lab report |
| L16 | Routing fundamentals & ICMP | Forwarding vs routing; routing tables, longest-prefix match; static routes; distance-vector vs link-state concepts; DV counting-to-infinity and fixes; IGP vs EGP; ICMP: echo, unreachable, TTL, traceroute's tricks; | BGP as the inter-domain EGP — a structural look (enr); policy routing (enr) | LAB-07: static routing + `traceroute` dissection on a 3-router VM topology | CS-02 milestone 1 | 10/50/5/45/10 | C3–C4 | CLO3, CLO4, CLO6 | Lab report; CS-02 addressing plan due |

### Module 4 — Transport Layer (L17–L20, 8 h)

> Concept ≈ 65 min, activity ≈ 40 min per lecture; this module is lab-heavy by design
> (programming + measurement). Feeds CLO4, CLO5, CLO6, CLO7.

| # | Lecture title | Core topics | Enrichment topics (enr) | Lab / GA | CS | M&C | Bloom | CLOs | Assessment artifact |
|---|---|---|---|---|---|---|---|---|---|
| L17 | UDP & the transport layer's job | Why a transport layer; ports & multiplexing; UDP datagram format; UDP vs IP demux; socket programming model (client/server); when UDP is the right choice | QUIC as UDP-based transport (enr); UDP checksum weaknesses (enr) | LAB-08: build a UDP chat/file-transfer client & server (Python) | — | 10/45/5/55/10 | C3 | CLO4, CLO5 | Working code + short demo |
| L18 | TCP essentials: connections & reliable delivery | TCP segment format; 3-way handshake & teardown; sequence/acknowledgment numbers; reliability: retransmission, RTT estimation & RTO, cumulative ACKs; connection states | Wireshark TCP conversation filters & statistics views (enr) | GA-18: handshake & retransmission dissection on a real trace | — | 10/55/5/40/10 | C2–C4 | CLO4, CLO5 | Exit ticket; annotated trace excerpt |
| L19 | TCP flow & congestion control | Sliding window, receiver window, in-flight data; slow start, congestion avoidance, fast retransmit/recovery; RTT/throughput math; bufferbloat & queueing delay in practice; intro to congestion-control variants | CUBIC vs BBR (enr); ECN (enr) | LAB-09: TCP performance with `netem` (delay/loss/bandwidth sweeps, interpret results) | — | 10/50/5/50/10 | C4 | CLO5, CLO6 | Lab report with graphs & interpretation |
| L20 | Programming the transport layer: reliability over UDP | Why build your own reliability (control, UDP-based apps); ACK schemes, timeouts, sequencing design; comparing your protocol's behavior to TCP; case walkthrough | QUIC's design answers compared (enr); FEC-based transports (enr) | LAB-10/11 (assign project): reliable transport over UDP — design + implement | — | 10/50/5/50/10 | C5–C6 | CLO5, CLO6 | Project spec (graded milestone) |

### Module 5 — Application Layer & Network Services (L21–L23, 6 h)

> Concept ≈ 70 min, activity ≈ 35 min per lecture. Feeds CLO4, CLO7; security previews
> continue (L21, L22).

| # | Lecture title | Core topics | Enrichment topics (enr) | Lab / GA | CS | M&C | Bloom | CLOs | Assessment artifact |
|---|---|---|---|---|---|---|---|---|---|
| L21 | DNS: the Internet's directory | Namespace & hierarchy; recursive vs iterative resolution; record types (A, AAAA, CNAME, MX, NS, TXT); caching & TTL; DNS security preview (poisoning, DoH/DoT concept) | DNSSEC concepts (enr); anycast DNS (enr) | GA-21: `dig`/`nslookup` drills + capture a full resolution | — | 10/55/5/40/10 | C3–C4 | CLO4, CLO7 | Exit ticket; resolution-path worksheet |
| L22 | DHCP deep dive, BOOTP & address management | DHCP message anatomy; options & vendor uses; lease renewal/T1/T2; conflicts & starvation (security thread); IPAM concepts | PXE boot (enr); DHCP snooping preview (enr) | GA-22: dissect DORA on a live capture; small IPAM exercise | — | 10/50/5/45/10 | C3–C4 | CLO4, CLO7 | Exit ticket; DORA annotated trace |
| L23 | Core application protocols: HTTP/1.1 → HTTP/3, SMTP & SSH | HTTP request/response, methods, status codes; HTTP/1.1 keep-alive & pipelining → HTTP/2 multiplexing → HTTP/3/QUIC; SMTP flow; SSH as a secured remote shell (transport over TCP, auth); API-era patterns | WebSockets & server push (enr); gRPC/HTTP2 internals (enr) | LAB-12: capture & compare HTTP/1.1 vs HTTP/2 vs HTTP/3; SMTP & SSH session dissection | CS-03 kickoff (Meridian service outage; diagnose from traces) | 10/55/5/40/10 | C3–C4 | CLO4, CLO6 | Lab worksheet; CS-03 evidence log opened |

### Module 6 — Network Security (L24–L26, 6 h)

> Concept ≈ 70 min, activity ≈ 35 min per lecture. Consolidates the security thread from
> L11, L12, L21, L22. Feeds CLO7.

| # | Lecture title | Core topics | Enrichment topics (enr) | Lab / GA | CS | M&C | Bloom | CLOs | Assessment artifact |
|---|---|---|---|---|---|---|---|---|---|
| L24 | Security principles & cryptographic building blocks | CIA triad; threat taxonomy (spoofing, eavesdropping, MITM, DoS/DDoS); crypto goals (confidentiality, integrity, authentication); symmetric/asymmetric basics; hashing; TLS: handshake shape, certificates, why it defeats MITM | Key exchange math light-touch (enr); certificate transparency (enr) | GA-24: read a real certificate chain; TLS handshake dissection worksheet | — | 10/55/5/40/10 | C3–C4 | CLO7 | Exit ticket; worksheet |
| L25 | Perimeter & internal defenses: firewalls, segmentation, VPNs | Firewall types (packet filter, stateful, NGFW concept); zones & policy writing; DMZ design; IDS/IPS: signatures vs anomalies, placement; VPN tunneling (site-to-site, remote access) | Zero-trust architecture ideas (enr); WAF (enr) | LAB-13: firewalls & VPN lab (VM: nftables/iptables rules + site-to-site VPN) | — | 10/50/5/45/10 | C4–C5 | CLO7 | Lab report with policy justifications |
| L26 | Attack & defense case workshop | Walkthroughs: ARP spoofing, DNS poisoning, DHCP starvation, TCP SYN flood; detection signals; layered defenses & residual risk; incident response basics | Honeypots (enr); threat modeling intro (enr) | GA-26: emulate a benign SYN-flood pattern in the VM lab; analyze & defend | CS-03 milestone 2 | 10/45/5/55/10 | C5 | CLO4, CLO7 | Workshop defense plan; CS-03 diagnosis due |

### Module 7 — Operations, Monitoring & Cloud (L27–L29, 6 h)

> Concept ≈ 60 min, activity ≈ 45 min per lecture. Feeds CLO5, CLO6, CLO7.

| # | Lecture title | Core topics | Enrichment topics (enr) | Lab / GA | CS | M&C | Bloom | CLOs | Assessment artifact |
|---|---|---|---|---|---|---|---|---|---|
| L27 | Cloud & virtual networking | Hypervisor & container networking (bridges, vNICs, overlay concept); VPC/VNet model: subnets, route tables, security groups vs ACLs; load balancers (L4 vs L7); hybrid connectivity concept | Cloud-interconnect pricing models (enr); service meshes (enr) | GA-27: build a mini-VPC in a VM lab (subnets, NAT, security rules) | — | 10/50/5/50/10 | C3–C4 | CLO3, CLO6 | Exit ticket; GA submission |
| L28 | Data-plane & SDN: programmable networks | Control/data plane separation; OpenFlow concept; SDN controller model; network functions virtualization; intent-based networking concept; data-science angle: telemetry as data streams | P4 pipeline concept (enr); SD-WAN (enr) | GA-28: SDN/telemetry demo + flow-record analysis exercise | — | 10/55/5/40/10 | C3–C4 | CLO1, CLO6 | Exit ticket; worksheet |
| L29 | Monitoring, telemetry & systematic troubleshooting | Monitoring stack (polling vs streaming, metrics/logs/traces); SNMP & flow telemetry (NetFlow/IPFIX); alerting & baselines; a repeatable troubleshooting methodology (observe → hypothesize → test → narrow); documentation | Observability tooling landscape (enr); synthetic monitoring (enr) | LAB-14: build a small monitoring dashboard + run a fault-injection drill | CS-03 wrap | 10/45/5/55/10 | C4–C5 | CLO5, CLO6, CLO7 | Lab report; CS-03 RCA report due |

### Module 8 — Integration & Capstone (L30–L32, 6 h)

> Concept ≈ 50 min, activity ≈ 55 min per lecture; sessions are workshop-style. Feeds CLO6,
> CLO8.

| # | Lecture title | Core topics | Enrichment topics (enr) | Lab / GA | CS | M&C | Bloom | CLOs | Assessment artifact |
|---|---|---|---|---|---|---|---|---|---|
| L30 | Mobile & wireless enterprise networking | Cellular generations concept (4G/5G headlines, handover); mobile IP problem framing; enterprise Wi-Fi design (roaming, RF planning basics, RADIUS/802.1X revisit); mobile-first design constraints | Network slicing (enr); private 5G (enr) | GA-30: design a campus wireless rollout worksheet | — | 10/50/5/50/10 | C3–C4 | CLO2, CLO6 | Exit ticket; design worksheet |
| L31 | Enterprise design & the data-science connection | Design methodology: requirements → topology → addressing → policy → documentation; HA patterns (redundancy, failover); data-science in networking: traffic classification, anomaly detection framing, capacity forecasting, measurement bias & ethics | NetDevOps/IaC idea (enr); certification paths overview (enr, vendor-neutral framing) | GA-31: full-network design review workshop (peer critique) | CS-04 design review (brief was due L26; defense L32) | 10/50/5/50/10 | C5–C6 | CLO6, CLO8 | Peer-review sheet; CS-04 design brief |
| L32 | Capstone workshop, presentations & course synthesis | In-class capstone build clinics; team presentations & defense; course-wide synthesis map (every topic on one diagram); exam guidance & review | Career/industry panels (enr) | Capstone build + present (in lieu of lab) | CS-04 milestone: capstone defense | 10/45/5/55/10 | C6 | CLO6, CLO8 | Capstone report, build, dashboard, presentation |

---

## Milestones & assessment anchors

| Week | Lecture | Academic event |
|---|---|---|
| 4 | L08 | Quiz 1 window opens (Modules 1–2 core to date) |
| 8 | L16 | **Midterm examination** (in lecture, 90 min, Modules 1–3) |
| 12 | L24 | Quiz 2 window opens (Modules 4–5 + transport project) |
| 13 | L26 | **Group project report due** (capstone stage 2 + CS-04 brief) |
| 16 | — | **Final examination** (cumulative, Modules 1–8, emphasis on 4–8) |

Capstone checkpoints and full due-date table: [`assessment-strategy.md`](assessment-strategy.md).

## Progression & dependency map

```
L01 ─ L02 ─ L03 ─ L04          (M1: foundations; everything depends on this chain)
   │
   ├─ L05 ─ L06 ─ L07 ─ L08 ─ L09 ─ L10 ─ L11   (M2: physical→link→LAN→WLAN)
   │                                 │
   │                                 └─ L12 ─ L13 ─ L14 ─ L15 ─ L16   (M3: IP, ARP, subnetting, DHCP/NAT, IPv6, routing)
   │                                                              │
   │                                                              └─ L17 ─ L18 ─ L19 ─ L20   (M4: transport)
   │                                                                           │
   │                                                                           └─ L21 ─ L22 ─ L23   (M5: DNS, DHCP deep dive, apps)
   │                                                                                        │
   │                                                                                        └─ L24 ─ L25 ─ L26   (M6: security)
   │                                                                                                       │
   │                                                                                                       └─ L27 ─ L28 ─ L29   (M7: cloud, SDN, monitoring)
   │                                                                                                                      │
   │                                                                                                                      └─ L30 ─ L31 ─ L32   (M8: mobile, design, capstone)
   └─ CS-01 (L03/L04) ─ CS-02 (L11–L16) ─ CS-03 (L23–L29) ─ CS-04 (L26→L32, capstone)
```

Hard dependencies to respect when reordering: L13 (subnetting) requires L12 (IP addressing);
L16 (routing) requires L13–L14; L18–L20 (TCP) require L17; L23 (HTTP/3) benefits from L20;
L26 (attack workshop) requires L12, L21, L22, L18; L27–L29 require Module 3–4 core; L32
requires all modules. Enrichment topics carry no dependencies.

## Load-balancing notes

- The heaviest student weeks are L13 (subnetting problem set), L19 (netem lab report), L20→L23
  window (reliable-transport project), and L29 (monitoring lab + CS-03 RCA). The assessment
  strategy deliberately keeps **no other major deliverable due in those weeks**.
- If the cohort is strong in programming, L20–L23 can absorb more Python; if weaker, GA-03a
  scaffolding in Module 1 should be expanded instead of adding new labs later.
- Modules 6–8 reduce lecture-time concept load to make room for capstone supervision; do not
  reintroduce new protocol detail there beyond what is scheduled.
