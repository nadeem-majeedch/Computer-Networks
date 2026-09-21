# Final Examination — Student Paper

| Field | Value |
|---|---|
| Course | Computer Networks — Final (cumulative; emphasis Modules 4–8) |
| Duration / marks | **120 minutes (proposed — strategy §3.8 fixes format, not duration) · 70 marks** (A 21 · B 28 · C 21) |
| Aids | Formula sheet provided (last page) · non-programmable calculator ⚠ per university rules · **no devices** |
| Integrity | Individual, closed-book — [`../academic-integrity.md`](../academic-integrity.md) §4 |
| Evidence note | All excerpts are **synthetic, written for this exam, internally consistent** |

Answer **all** questions. Show working — method marks survive arithmetic failures.

## Section A — Selected response & short answer (21 marks)

**A1–A6 (1 mark each).** Circle one answer.

**A1.** HTTP/3 changes the transport to:
(a) SCTP (b) QUIC over UDP (c) QUIC over TCP (d) HTTP over raw IP

**A2.** A stateful firewall's "allow established" rule admits a packet because:
(a) its port is well-known (b) it belongs to a flow the firewall saw initiated
(c) its checksum passes (d) it comes from a VPN

**A3.** A DNS record's TTL controls:
(a) the query timeout (b) how long resolvers may cache it (c) the server's lease
(d) the zone's size

**A4.** During a controller outage, an SDN switch typically:
(a) stops forwarding everything (b) keeps forwarding by its installed rules
(c) reverts to learning bridges (d) reboots into standalone mode

**A5.** At DHCP renewal time T1 (50% of lease), a client:
(a) re-enters discovery (b) unicasts a renewal to its original server
(c) self-assigns a link-local (d) broadcasts for any server

**A6.** HTTP/2's residual head-of-line blocking lives:
(a) in the browser cache (b) at the TCP layer (c) in DNS (d) in TLS 1.3 only

**A7 (2).** One sentence each: what flow control protects and what congestion control
protects, naming each window.

**A8 (2).** Why must a SLAAC host run duplicate address detection before using its
new address?

**A9 (2).** Name the three pieces of a NAT mapping's state and the event that removes
it.

**A10 (2).** What does DNSSEC cryptographically guarantee, and name one attack it
does **not** stop.

**A11 (2.** A browser warns "certificate signed by unknown authority." Explain the
failure in chain-of-trust terms (one sentence).

**A12 (2).** A lecture-hall AP serves 60 clients with strong signal yet poor
throughput. Name the limiting resource and the one-sentence mechanism.

## Section B — Problems (28 marks)

**B1 — Addressing (6).** Given `10.0.0.0/21`:
(a) usable host count (1)
(b) split into two equal /22 subnets: prefixes + ranges (2)
(c) smallest prefix for 60 hosts (1)
(d) is 10.0.5.200 inside the *second* of your two subnets? show the range test (2)

**B2 — TCP behavior (8).**
(a) BDP of 1 Gb/s at 40 ms RTT, in MB (2)
(b) slow start from 1 MSS to 32 MSS without loss: how many RTTs? (2)
(c) loss at cwnd = 20 MSS under the course's simplified rules: new ssthresh and cwnd (2)
(d) a transfer sustains 4 Mb/s at 50 ms RTT on a loss-free 1 Gb/s path: the implied
window, and which mechanism to inspect first (2)

**B3 — DNS & DHCP (6).**
(a) A recursive resolver with an empty cache resolves `cs.example.edu`: list its
queries in order and what each answer returns (3)
(b) A client's lease reaches T2 (87.5%) with the original server down: what does the
client do, and what happens at expiry if no server answers? (3)

**B4 — Firewalls & VPN (8).**
(a) Rule list (top-first): (1) deny 10.9.0.0/16 → 10.9.5.0/24:22 (2) allow
10.9.0.0/16 → 10.9.5.0/24:any. Result for 10.9.2.8 → 10.9.5.1:22, and the ordering
principle it illustrates (4)
(b) A site-to-site VPN joins HQ 10.20.0.0/22 and branch 10.30.0.0/24. State which
subnets the tunnel policy must include, what remains visible on the public path, and
one thing the VPN does **not** authenticate (4)

## Section C — Analysis & synthesis (21 marks)

**C1 (9).** Excerpt (synthetic) — client C→S bulk send:

```text
t=0.000  C→S [PSH,ACK] seq=1000 len=1460
t=0.001  C→S [PSH,ACK] seq=2460 len=1460
t=0.002  C→S [PSH,ACK] seq=3920 len=1460
t=0.003  C→S [PSH,ACK] seq=5380 len=1460
t=0.004  C→S [PSH,ACK] seq=6840 len=1460
t=0.050  S→C [ACK] ack=2460
t=0.052  S→C [ACK] ack=2460
t=0.054  S→C [ACK] ack=2460
t=0.056  S→C [ACK] ack=2460
t=0.057  C→S [PSH,ACK] seq=2460 len=1460
t=0.107  S→C [ACK] ack=8300
```

(i) Which segment was lost, and what evidence convicts it? (2)
(ii) Which TCP mechanism fired, and how many duplicate ACKs did it need? (3)
(iii) What does `ack=8300` assert, and what does it prove about the receiver's
out-of-order buffering? (2)
(iv) Estimate the RTT from the retransmission pair, naming the pair. (2)

**C2 (6).** Excerpt (synthetic) — a client bootstraps a connection:

```text
t=0.000  broadcast: who-has 10.50.0.1? tell 10.50.0.24
t=0.001  10.50.0.1 at 0c:5b:8f:1a:00:01 → 10.50.0.24
t=0.010  10.50.0.24:53011 → 10.50.0.1:53  Q: app.internal.corp A
t=0.012  10.50.0.1:53 → 10.50.0.24:53011  A: app.internal.corp A 10.50.7.9
t=0.020  10.50.0.24 → 10.50.7.9 [SYN] seq=0
```

(i) Identify the four protocol stages in order (2)
(ii) State one fact each stage proves about the network (4)

**C3 (6).** Synthesis: a staff laptop fetches `https://portal.internal.corp/` from an
internal server on another VLAN. List, **in order**, the decision points the request
crosses (DNS, L2 gateway, inter-VLAN policy, routing, TLS, application) and give one
sentence on what each contributes. (1 mark per point, coherence of order matters)

---

*Formula sheet (provided):* Nyquist C = 2B log₂M · Shannon C = B log₂(1+SNR) ·
SNR(dB) = 10 log₁₀(SNR) · serialization = bits/link-rate · usable hosts = 2^h − 2 ·
BDP = rate × RTT · rate ≈ window/RTT
