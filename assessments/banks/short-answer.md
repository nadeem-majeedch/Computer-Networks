# Question Bank — Short Answer

| Field | Value |
|---|---|
| Scope | 2–5 sentence written answers; tests precise explanation, not prose volume |
| Tagging | `[Difficulty|CLO|Source]` |
| Key | fenced at end — do not distribute |

## Questions

**SA-01 [B|CLO1|L02]** Define encapsulation and name the PDU at each TCP/IP layer.
**SA-02 [B|CLO1|L01]** Explain the difference between delay and jitter with one example
each from a video call.
**SA-03 [I|CLO2|L05]** Why can't you "fix" a Shannon-limited link by re-encoding with
more signal levels? What *does* raise the Shannon ceiling?
**SA-04 [I|CLO2|L06]** Compare checksum and CRC: mechanism difference and detection
strength difference.
**SA-05 [I|CLO2|L08]** Describe how a switch learns and what it does with an unknown
destination, then state when flooding stops.
**SA-06 [I|CLO2|L09]** Explain why VLANs improve security even though hosts can still
send frames to the switch.
**SA-07 [I|CLO2|L10]** Why do Wi-Fi stations back off randomly rather than waiting a
fixed slot?
**SA-08 [I|CLO3|L12]** A host ARPs for an off-subnet destination's *gateway*. Explain
the two addresses (L2, L3) this produces and why both are needed.
**SA-09 [I|CLO3|L13]** Explain why VLSM reduces waste versus fixed-length subnetting,
using a 2-host link as your example.
**SA-10 [I|CLO4|L14]** NAT: name the three pieces of state per mapping and the event
that removes the mapping.
**SA-11 [I|CLO3|L15]** Why is duplicate address detection (DAD) required for SLAAC?
**SA-12 [I|CLO4|L16]** Explain longest-prefix match and why a default route never
outranks a specific one.
**SA-13 [I|CLO4|L17]** Give one application that must use UDP and one that must use
TCP, with the property that forces the choice.
**SA-14 [I|CLO4|L18]** Why does the TCP handshake randomize initial sequence numbers?
**SA-15 [I|CLO4|L19]** Explain the receiver-window vs congestion-window distinction
and how the sender combines them.
**SA-16 [I|CLO4|L21]** Explain the difference between a recursive and an authoritative
DNS server's role.
**SA-17 [I|CLO4|L22]** Why do DHCP leases expire at all? What would go wrong with
permanent leases in a 300-device school?
**SA-18 [I|CLO4|L23]** HTTP/2 multiplexing: explain what "streams" prevent that
pipelining could not.
**SA-19 [I|CLO7|L24]** Explain why TLS needs certificates: what breaks if clients
accepted any public key?
**SA-20 [I|CLO7|L25]** Explain the difference between what a firewall permits and what
a VPN protects.
**SA-21 [I|CLO6|L27]** Explain why containers need NAT for outbound traffic by
default.
**SA-22 [I|CLO6|L28]** Contrast per-switch learning (traditional L2) with controller-
programmed forwarding (SDN) on *who* decides and *when*.
**SA-23 [I|CLO6|L29]** Why is a single threshold alert on utilization weaker than a
baseline-deviation alert? Give the failure mode of each.
**SA-24 [I|CLO5|L31]** A nightly job moves 100 000 small files. Explain the
round-trip-dominated behavior and the packing fix.
**SA-25 [I|CLO6|L31]** In enterprise design, why does "default deny between zones"
produce safer failure than "default allow with blocks"?
**SA-26 [E|CLO6|L32]** Defend or refute: "Latency, not bandwidth, is the modern
bottleneck for distributed data systems." Use one cloud-workload example.

**SA-27 [A|CLO6|L19/L29]** A transfer's throughput drops ~40% exactly when a nightly
backup starts, though ping stays clean (no loss). Explain the likely mechanism in
3–4 sentences using the window–RTT relationship.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**SA-01.** Encapsulation: each layer wraps the upper layer's PDU with its own header
(and sometimes trailer). Message → segment → datagram/packet → frame (→ bits).
**SA-02.** Delay: absolute time a packet needs (mouth-to-ear latency example). Jitter:
variation of that delay across packets (freeze-then-jump video example — late frames
arrive in bursts).
**SA-03.** More levels are capped by *noise*: at SNR 15 dB, more levels just split the
same noise-corrupted signal. Shannon's ceiling rises only with bandwidth or SNR
(better medium/amplification/less noise).
**SA-04.** Checksum: additive sum of words — cheap, catches many errors but blind to
compensating patterns. CRC: polynomial division — detects all bursts shorter than the
polynomial degree and most longer ones.
**SA-05.** Learns source MAC↔port per frame (and ages entries); unknown destination →
flood all ports in the VLAN except ingress. Flooding for M stops when M's own reply
is learned (or a static entry/aging refresh exists).
**SA-06.** Because reachability between VLANs now *requires* the L3 device, which
enforces policy: broadcasts, sniffing, and most L2 attacks cannot cross the boundary
— the switch itself will not bridge the VLANs.
**SA-07.** Collisions can't be detected reliably on radio (can't hear while
transmitting), so avoidance + random backoff spreads retries: fixed slots would
synchronize contenders into repeated collisions.
**SA-08.** L2 (frame dst MAC) = gateway's MAC; L3 (IP header dst) = the remote
destination. Both needed: MAC delivers one hop on the local link; IP address survives
end-to-end and routes onward.
**SA-09.** Fixed-length: a /26-per-net plan burns 62 addresses for a 2-host link.
VLSM: the link takes a /30 (4 addresses, 2 usable) — waste drops from ~60 to 2.
**SA-10.** State per mapping: inside (IP:port) ↔ outside (IP:port), protocol, timeout.
Removed: timeout expiry (or explicit teardown/connection close).
**SA-11.** SLAAC builds addresses without a server; two hosts could self-assign the
same address on a link. DAD probes the candidate address first and aborts on
duplication.
**SA-12.** The router picks the *most specific* matching prefix (most leading bits);
a default route matches everything with the shortest prefix (0 bits), so any specific
route outranks it — it only wins when nothing else matches.
**SA-13.** Must-UDP: live voice/video — retransmitting a late packet is worse than
dropping it (timeliness). Must-TCP: file transfer/banking — correctness requires
ordered, complete delivery.
**SA-14.** Predictable ISNs let an off-path attacker forge in-window segments (hijack
or inject); randomness makes guessing the sequence space infeasible.
**SA-15.** rwnd = receiver's buffer space (protects the receiver); cwnd = sender's
network estimate (protects the network). In-flight limit = min(cwnd, rwnd).
**SA-16.** Recursive resolver: does the full lookup on the client's behalf and caches.
Authoritative server: owns a zone and gives definitive answers for it — never chases
referrals.
**SA-17.** Expiry recycles unused addresses — the pool matches *concurrent* devices,
not total enrolled ones. Permanent leases in a school: graduates' phones, retired
printers etc. hold addresses forever → pool exhaustion.
**SA-18.** Streams interleave requests/responses concurrently on one connection —
no request waits for the previous *response* (pipelining's head-of-line stall at L7).
**SA-19.** Certificates bind a name to a public key via a CA the client already
trusts. Without that, any attacker can present their own key for the victim's name —
no server authentication at all.
**SA-20.** A firewall controls *which* flows may pass a boundary; a VPN protects
*content* across untrusted transit (confidentiality/integrity). A VPN does not make a
flow permitted; a firewall does not make a flow secret.
**SA-21.** Pod IPs are private to the host and meaningless off-box; the node SNATs
egress so replies can return to the node, which maps them back to the pod.
**SA-22.** Traditional: each switch decides *locally and continuously* (learning,
protocol timers). SDN: a controller computes decisions *globally* and pushes
match/action rules; switches only execute.
**SA-23.** Static threshold: pages on normal-but-loud nights (backup), misses slow
degradation below the line. Baseline deviation: adapts to time-of-day shape; its
failure mode is blind to genuinely novel-but-in-baseline patterns. Each failure named.
**SA-24.** Each file costs multiple round trips (open, write, close, metadata) × RTT;
100 000 × even 2 ms = 200 s of pure waiting per worker. Packing into archives/objects
amortizes one round trip over megabytes.
**SA-25.** Default deny: an unconfigured service fails *closed* — a forgotten rule
leaves it unreachable, not exposed. Default allow: the same mistake silently publishes
it between zones.
**SA-26.** Defensible: many cloud workloads are RTT-bound (chatty microservices, small
object reads, cross-region sync) where adding bandwidth changes nothing — e.g., 100k
small-file training reads on a 10 Gb/s link stay slow at any bandwidth; cutting RTT or
round trips wins. Refutation acceptable only with a genuinely bandwidth-bound example
(backup flooding, model checkpoint pushes) — full credit requires naming *which regime
each example belongs to*.
**SA-27.** The backup fills router/switch queues on the shared path, inflating RTT
(e.g., 20 ms → 80 ms) before any loss occurs — which is why ping stays "clean"
(loss-free but slower). With a fixed window, rate ≈ window/RTT, so 4× the RTT is
~¼ the throughput — the observed ~40% drop fits a smaller RTT inflation (or partial
window growth). Full-credit answers name the direction of the fix: QoS-class the
backups, or grow the window to cover the new BDP.
