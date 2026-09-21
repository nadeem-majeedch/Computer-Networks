# Question Bank — Conceptual

| Field | Value |
|---|---|
| Scope | Architecture/layering · physical & link · internet/transport · security & operations |
| Tagging | `[Difficulty|CLO|Source]` — B/I/A/E tiers per assessments/README.md §3 |
| Key | fenced at end — do not distribute. Items are course-level; standards-sensitive answers cite the source in the key |
| Reuse rule | Differs from quiz/review/exam items by scenario or reasoning step (README §3) |

## B1 — Architecture, layering, fundamentals

**C-01 [B|CLO1|L01]** Why do protocols, not vendor choice, define a "network"?
**C-02 [B|CLO1|L01]** Give one advantage and one cost of packet switching versus circuit switching for a live voice call.
**C-03 [I|CLO1|L02]** A debug tool prints "L4 header, L3 header, L2 header, payload." Which direction of encapsulation is it describing, and what device typically adds the L2 header?
**C-04 [I|CLO1|L02]** The hourglass model puts IP at the narrow waist. State the engineering benefit and the lock-in cost.
**C-05 [I|CLO1|L03]** An app uses a library that opens sockets. Which layer does the app *not* implement, and which header does it still author?
**C-06 [A|CLO1|L02]** Argue for or against "OSI is obsolete" using one correct and one incorrect claim commonly attached to that statement.

## B2 — Physical, link, switching

**C-07 [B|CLO2|L05]** Why does adding spectrum (Hz) raise capacity under both Nyquist and Shannon?
**C-08 [I|CLO2|L05]** Fiber vs copper: which wins on (i) EMI immunity, (ii) distance per segment, (iii) per-port cost — and why is copper still dominant at desk level?
**C-09 [I|CLO2|L06]** Parity catches single-bit flips. Give an error pattern it cannot catch, and what property the pattern has.
**C-10 [I|CLO2|L07]** A capture shows frames with FCS errors from one cable. Where does the switch place them, and why doesn't it forward them?
**C-11 [I|CLO2|L08]** State the difference between a collision domain and a broadcast domain with one artifact each.
**C-12 [A|CLO6|L08]** Two switches, two parallel links, no STP — describe the exact failure sequence for a broadcast frame.
**C-13 [I|CLO2|L09]** Why can two VLANs share one switch chassis safely but not one trunk with mismatched native VLANs?
**C-14 [I|CLO2|L10]** Wi-Fi retransmits lost frames at L2. Why is that necessary where wired Ethernet's frames rarely need it?

## B3 — Internet layer, transport, applications

**C-15 [B|CLO3|L12]** What makes an IP address "logical" versus a MAC address "physical"?
**C-16 [I|CLO4|L12]** ARP resolves IP→MAC on one link. Why does the design not extend ARP across routers?
**C-17 [I|CLO3|L13]** Why does the /30 prefix fit point-to-point links "exactly," and what does a /31 give modern stacks?
**C-18 [I|CLO4|L14]** NAT breaks which communication patterns, and which protocol family needed explicit workarounds?
**C-19 [I|CLO3|L15]** IPv6 removed broadcast. Name its replacement class and one protocol that uses it.
**C-20 [I|CLO4|L16]** Longest-prefix match: why does it make route summaries safe in the presence of exceptions?
**C-21 [B|CLO4|L17]** Why is UDP "connectionless," and what does an app give up versus TCP?
**C-22 [I|CLO4|L18]** TCP's cumulative ACK: one lost segment delays ACKs for all later data at the receiver. How do SACKs reduce the damage?
**C-23 [I|CLO4|L19]** Slow start doubles cwnd per RTT; congestion avoidance adds one MSS per RTT. Why does each growth law fit its phase?
**C-24 [I|CLO4|L21]** A resolver caches a record at TTL expiry boundary. What are the two consistent behaviors (lazy vs eager expiry) and why do both satisfy the standard's intent?
**C-25 [I|CLO4|L23]** HTTP/2 multiplexing fixed L7 head-of-line blocking but kept a transport-level one. Name it and the mechanism.
**C-26 [A|CLO6|L23]** A CDN serves your site from 30 cities. Which DNS and TCP behaviors make the "same URL" fast everywhere? Name both mechanisms.

## B4 — Security, operations, data-science networking

**C-27 [B|CLO7|L24]** Hash → integrity; encryption → confidentiality; signature → authenticity. Which goal needs *two* of these together?
**C-28 [I|CLO7|L25]** Stateful firewall: why is "allow established" not equivalent to "allow all TCP"?
**C-29 [I|CLO7|L25]** VPN: what does a site-to-site tunnel protect that a firewall cannot, and what does it *not* authenticate?
**C-30 [I|CLO6|L27]** A pod's outbound traffic NATs to the node IP. Which operational property improves, and which debugging property gets harder?
**C-31 [I|CLO6|L28]** SDN centralized control: state one consistency benefit and one blast-radius risk in one sentence each.
**C-32 [I|CLO6|L29]** Why do utilization alerts without baselines page on backup nights and stay silent on real incidents?
**C-33 [I|CLO5|L31]** A data-science team moves many small files nightly. State the network-level reason throughput stalls and the storage-level fix.
**C-34 [A|CLO6|L31]** Your ML cluster shares a 25 Gb/s fabric with backups. Which two design controls prevent backup windows from corrupting training throughput measurements?
**C-35 [E|CLO6|L29/L32]** A "healthy" dashboard shows green during a brownout where RTT doubled but no link saturated. Which two metrics were missing from the dashboard, and why does green mislead?

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**C-01.** Interoperability comes from agreed message formats and state machines (open
standards), so independent implementations interwork regardless of vendor. **C-02.**
Advantage: no dedicated circuit per call — capacity scales with demand. Cost:
per-packet jitter/loss handling must be added (buffers, prioritization) since delivery
is best-effort. **C-03.** It is describing *decapsulation on receipt* (innermost to
outermost is receive order); the first router/host egress device adds the L2 header
per link. **C-04.** Benefit: any transport and any link interwork through one narrow
abstraction (innovation at the edges). Cost: the waist is hard to replace — IPv4/IPv6
transition friction. **C-05.** The app does not implement L2–L4 (OS does); it still
authors the application-layer message (HTTP headers, payload). **C-06.** Correct
claim: the OSI *protocol suite* lost to TCP/IP. Incorrect claim: "the OSI *model* is
unused" — it remains the shared vocabulary. Any defensible pair with labels. **C-07.**
More Hz → more symbols/s (Nyquist 2B) and more independent b/s budget for a given SNR
(Shannon scales linearly in B). **C-08.** Fiber wins (i) immunity — light is not
charge-coupled; (ii) distance — low attenuation/km; copper wins (iii) per-port cost —
ubiquitous PHYs, cheap cabling and patching at ≤100 m. **C-09.** Any even number of
flips in one row/column pattern, e.g., two bits flipped in the same row: row and
column parities stay valid — the property is "even weight." **C-10.** Dropped on
FCS check; not forwarded (not learned from) because the frame may be corrupted
including addresses. **C-11.** Collision domain: one full-duplex switch port (artifact:
port counters). Broadcast domain: a VLAN (artifact: broadcast counter per VLAN). **C-12.**
Broadcast out both links → each switch re-floods on the other → exponential frame
duplication; FDB entries flap between ports as source MACs arrive alternately; CPU/
buffers saturate — the broadcast storm. **C-13.** VLANs isolate forwarding tables per
VLAN so frames never leak; a native-VLAN mismatch sends untagged frames into the
*wrong* VLAN on the far trunk — leakage by configuration, not isolation failure. **C-14.**
Wireless links are noisy/interference-prone at the air interface; unacknowledged
frames would be lost to apps. Ethernet's wired BER is far lower, and L4 handles the
residual losses. **C-15.** IP is assigned per network (topology-dependent, routable);
MAC is burned-in per NIC (device identity, L2-local meaning). **C-16.** ARP scopes to
the broadcast domain; across routers the next-hop MAC is the *router's*, per-link —
an inter-router ARP would have no common L2 medium. **C-17.** /30: 4 addresses − 2
(network, broadcast) = 2 hosts = exactly the two routers. /31: modern stacks treat it
as point-to-point (RFC 3021) needing no network/broadcast reservation. **C-18.**
Inbound-initiated connections (no pre-existing mapping) and protocols embedding
addresses/ports in payloads (classic FTP, SIP) — hence ALGs and UPnP. **C-19.**
Multicast (solicited-node, ff02::1); used by NDP (IPv6's ARP/RS/RA successor). **C-20.**
A summary is just a shorter prefix; a longer, more-specific route for an exception
always outranks it at lookup, so aggregation coexists with exceptions. **C-21.**
No handshake or per-connection state: datagrams are independent. Given up: ordering,
reliability, congestion control, flow control — the app owns them if needed. **C-22.**
SACK reports received ranges beyond the hole, so the sender retransmits *only* the
gap instead of rewinding the window. **C-23.** Slow start: unknown network capacity —
exponential probing converges fast but risks overload, so it stops at ssthresh;
avoidance: near capacity — linear growth grows congestion cautiously. **C-24.** Lazy:
serve until TTL boundary passes, then refetch; eager: refetch when TTL hits. RFC 1035
sets the *maximum* caching interval; both behaviors honor it (intent: bound staleness).
**C-25.** TCP-level head-of-line blocking: a lost TCP segment stalls delivery of *all*
multiplexed streams until retransmission arrives; QUIC (HTTP/3) fixes per-stream. **C-26.**
DNS: authoritative servers answer with the *nearest* PoP's address (geo/latency-aware
resolution). TCP: connection terminates at that nearby PoP; the CDN's backbone
(fetch-to-origin) is optimized — the client's RTT is short everywhere. **C-27.**
Authenticity with integrity — a signature (hash signed) needs both; also "confidential
AND tamper-evident" (encrypt-then-MAC) acceptable with justification. **C-28.** State
tracking distinguishes packets belonging to flows initiated *from inside* (SYN seen)
from forged inbound packets claiming ESTABLISHED flags — a plain port rule cannot.
**C-29.** Protects: confidentiality/integrity of traffic across untrusted transit
(firewalls only filter at the perimeter). Does not authenticate: endpoint users —
tunnel peers authenticate machines/networks; app auth remains separate. **C-30.**
Improves: address conservation and simple egress policy. Harder: mapping external
connections back to the right pod (shared IP:port state). **C-31.** Benefit: one
globally consistent view — no per-box rule drift or conflict. Risk: controller
outage freezes topology changes fabric-wide. **C-32.** Static thresholds ignore
diurnal/workload shape: backup night *is* 90% normally; a real incident that stays
under the threshold (e.g., 80% with new latency) pages nobody — baselines encode
"normal" per time-of-day. **C-33.** Per-file round trips (open/close, small writes)
serialize on RTT: 10k files × 2 ms RTT ≈ 20 s of pure latency per worker regardless
of bandwidth. Fix: object/archive packing or batched transfer (fewer round trips).
**C-34.** (i) QoS/queue separation: shape backups into their own class (priority or
bandwidth reservation) so training flows keep latency bounds; (ii) measurement
hygiene: schedule measurements outside backup windows or tag/classify flows so
per-class statistics are compared. **C-35.** Missing: path RTT/latency percentile
metrics and saturation-at-*lower-layer* indicators (queue depth, retransmits, airtime).
Green misleads because the dashboard's "health" = utilization only; brownout lived in
delay, not throughput.
